###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import argparse, sys, os, math

from .tuples import write_array, write_friend_array, read_array
from .legacy.run1 import Config as ConfigRun1
from .legacy.run2 import Config as ConfigRun2

import uproot
import importlib
import numpy as np
import awkward as ak

from .resampling import calib_transform, data_transform, get_or_create_template, resample_data

def get_template(filename, ranges) : 
    dim = uproot.concatenate(filename + ":DimTree")['bins'].to_numpy()
    maptree = uproot.concatenate(filename + ":MapTree")
    dens   = np.reshape(maptree['dens'].to_numpy(),   dim, 'F')
    inphsp = np.reshape(maptree['inphsp'].to_numpy(), dim, 'F')
    edges = [ np.linspace(rng[0], rng[1], b+1) for b,rng in zip(dim, ranges) ]
    return dens, edges

def legacy_resample(
  infilename, 
  outfilename = "out.root", 
  outtree = "tree", 
  pidgen = "pidgen", 
  stat = "stat", 
  ptvar = "pt1", 
  pvar = "p1", 
  etavar = "eta1", 
  ntrvar = "ntr1", 
  minpid = 0., 
  config = "K_MC15TuneV1_ProbNNK_Brunel", 
  dataset = "MagUp_2016", 
  variant = "default", 
  seed = 0, 
  ntrscale = 1., 
  library = "ak", 
  step_size = 50000, 
  friend = False, 
  ) : 

  if not infilename:
    print("Usage: PIDGen.py [options]")
    #  print "  For the usage example, look at pid_resample.sh file"
    print("  Available PID configs are: ")
    print("    For Run1 : ")
    for i in sorted(ConfigRun1.configs.keys()):
        print("      ", i)
    print("    For Run2 : ")
    for i in sorted(ConfigRun2.configs().keys()):
        print("      ", i)
    quit()

  if variant == "default":
    variant = "distrib"  # to do: change this name in CreatePIDPdf

  year = None
  run = None
  try:
    year = dataset.split("_")[1]
  except:
    print(
        'Dataset format "%s" not recognized. Should be {MagUp,MagDown}_[Year]'
        % dataset)
    quit()
  if year in ["2011", "2012"]:
    run = 1
  elif year in ["2015", "2016", "2017", "2018"]:
    run = 2
  else:
    print('Data taking year "%s" not recognized' % year)
    quit()

  print(year, run, dataset)

  if run == 1:
    calibfilename = ConfigRun1.eosrootdir + "/" + config + "/" + "%s_%s.root" % (
        dataset, variant)
    transform_forward = ConfigRun1.configs[config]['transform_forward']
    transform_backward = ConfigRun1.configs[config]['transform_backward']
    configs = ConfigRun1.configs
  else:
    calibfilename = ConfigRun2.eosrootdir + "/" + config + "/" + "%s_%s.root" % (
        dataset, variant)
    configs = ConfigRun2.configs()
    if 'gamma' in list(configs[config].keys()):
        gamma = configs[config]['gamma']
        if gamma < 0:
            transform_forward = "(1.-(1.-x)**%f)" % abs(gamma)
            transform_backward = "(1.-(1.-x)**%f)" % (1. / abs(gamma))
        else:
            transform_forward = "((x)**%f)" % abs(gamma)
            transform_backward = "((x)**%f)" % (1. / abs(gamma))
    else:
        transform_forward = configs[config]['transform_forward']
        transform_backward = configs[config]['transform_backward']

  pidmin = 0.
  pidmax = 1.
  if 'limits' in configs[config]:
    pidmin = configs[config]['limits'][0]
    pidmax = configs[config]['limits'][1]
  if minpid == None:
    minpid = pidmin
  else:
    minpid = float(minpid)
    if minpid < pidmin: minpid = pidmin

  # Calculate the minimum PID variable to generate (after transformation)
  x = pidmin
  pidmin = eval(transform_forward)
  x = pidmax
  pidmax = eval(transform_forward)
  x = minpid
  minpid = eval(transform_forward)

  ranges = [
    (pidmin, pidmax), 
    (5.5, 9.5), 
    (1.5, 5.5), 
    (3.0, 6.5)
  ]

  counts, edges = get_template(calibfilename, 4*[(0., 1.)])

  print(transform_forward)
  print(transform_backward)
  
  print(counts.shape)

  config = {
    "transform" : [
      "np.log(x)",
      "x", 
      "np.log(x)"
    ], 
    "normalise_methods" : ["scale", "scale", "scale"], 
    "normalise_ranges" : 3*[(0., 1.)],
  }

  scale_list = (1., 1., ntrscale)

  branches = [ptvar, etavar, ntrvar]

  data = uproot.concatenate(infilename, expressions = branches)
  array = np.stack([ data[ptvar].to_numpy(), data[etavar].to_numpy(), data[ntrvar].to_numpy()*1.0 ], axis = 1)

  print(array)
  print(array.shape)

  transformed_array = data_transform(array, config, scale_list)

  print(transformed_array)

  template = (counts, edges, [(None, ranges[0]), (None, ranges[1]), (None, ranges[2]), (None, ranges[3])])
  vardef = {
    "normalise_method" : "scale", 
    "transform_backward" : transform_backward,
    "data_range" : ranges[0], 
    "normalise_range" : (0., 1.), 
    "resample_bins" : 200, 
  }

  pid_arr, calib_stat = resample_data(transformed_array, config, vardef, template, verbose = True)

  print(pid_arr)
  print(calib_stat)

  output_arrays = [ pid_arr, calib_stat ]
  output_branches = [ pidgen, stat ]

  if not friend : 
    write_array(outfilename, np.asarray(np.concatenate(output_arrays, axis = 1)),
            branches = output_branches, input = infilename, tree = outtree, step_size = step_size, 
            library = library)
  else : 
    write_friend_array(outfilename, np.asarray(np.concatenate(output_arrays, axis = 1)), 
            branches = output_branches, tree = outtree )

legacy_resample("../../pidgen2_tests/edoardo/merged.root", outfilename = "out.root")
