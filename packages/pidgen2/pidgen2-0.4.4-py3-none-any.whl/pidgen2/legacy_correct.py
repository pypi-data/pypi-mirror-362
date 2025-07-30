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

from .legacy.run1 import Config as ConfigRun1
from .legacy.run2 import Config as ConfigRun2
from .legacy.run1 import ConfigMC as ConfigMCSim08
from .legacy.run1 import ConfigMCSim09 as ConfigMCSim09
from .legacy.run2 import ConfigMC as ConfigMCRun2

import sys

import uproot
import importlib
import numpy as np
import awkward as ak

from .tuples import write_array, write_friend_array, read_array
from .resampling import calib_transform, data_transform, correct_data

def get_template(filename, ranges) : 
    dim = uproot.concatenate(filename + ":DimTree")['bins'].to_numpy()
    maptree = uproot.concatenate(filename + ":MapTree")
    dens   = np.reshape(maptree['dens'].to_numpy(),   dim, 'F')
    inphsp = np.reshape(maptree['inphsp'].to_numpy(), dim, 'F')
    edges = [ np.linspace(rng[0], rng[1], b+1) for b,rng in zip(dim, ranges) ]
    return dens, edges

def legacy_correct(
  infilename = None, 
  outfilename = "out.root", 
  outtree = "tree", 
  pidvar = "p1_legacy_pidcorr",
  stat = "p1_legacy_pidstat", 
  mcstat = "p1_legacy_pidmcstat", 
  ptvar = "p1_pt", 
  pvar = "p1_p", 
  etavar = "p1_eta", 
  ntrvar = "ntr", 
  minpid = 0., 
  oldpidvar = "p1_pidv2", 
  conf = "pi_V2ProbNNpi", 
  dataset = "MagDown_2012", 
  variant = "default", 
  simversion = "sim09", 
  ntrscale = 1., 
  library = "ak", 
  step_size = 50000, 
  friend = False, 
  nan = -1000., 
  ) : 

  if not infilename:
    print("Usage: PIDCorr.py [options]")
    #  print "  For the usage example, look at pid_transform.sh file"
    print("  Available PID configs for Run1/sim08 are: ")
    for i in sorted(ConfigRun1.configs.keys()):
        if i in list(ConfigMCSim08.configs.keys()):
            print("    ", i)
    print("  Available PID configs for Run1/sim09 are: ")
    for i in sorted(ConfigRun1.configs.keys()):
        if i in list(ConfigMCSim09.configs.keys()):
            print("    ", i)
    print("  Available PID configs for Run2/sim09 are: ")
    for i in sorted(ConfigRun2.configs().keys()):
        if i in list(ConfigMCRun2.configs.keys()):
            print("    ", i)

    # Exit politely
    sys.exit(0)

  if simversion == "sim08":
    ConfigMC = ConfigMCSim08
    Config = ConfigRun1
  elif simversion == "sim09":
    ConfigMC = ConfigMCSim09
    Config = ConfigRun1
  elif simversion == "run2":
    ConfigMC = ConfigMCRun2
    Config = ConfigRun2
  else:
    print("Simulation version %s unknown" % simversion)
    sys.exit(1)

  if variant == "default":
    variant = "distrib"  # to do: change this name in CreatePIDPdf

  datapdf = Config.eosrootdir + "/" + conf + "/" + dataset + "_" + variant + ".root"
  simpdf = ConfigMC.eosrootdir + "/" + conf + "/" + dataset + "_" + variant + ".root"

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

  if run == 1:
    calibfilename = ConfigRun1.eosrootdir + "/" + conf + "/" + "%s_%s.root" % (
        dataset, variant)
    transform_forward = ConfigRun1.configs[conf]['transform_forward']
    transform_backward = ConfigRun1.configs[conf]['transform_backward']
    configs = ConfigRun1.configs
  else:
    calibfilename = ConfigRun2.eosrootdir + "/" + conf + "/" + "%s_%s.root" % (
        dataset, variant)
    configs = ConfigRun2.configs()
    if 'gamma' in list(configs[conf].keys()):
        gamma = configs[conf]['gamma']
        if gamma < 0:
            transform_forward = "(1.-(1.-x)**%f)" % abs(gamma)
            transform_backward = "(1.-(1.-x)**%f)" % (1. / abs(gamma))
        elif gamma == 1.:
            transform_forward = "x"
            transform_backward = "x"
        else:
            transform_forward = "((x)**%f)" % abs(gamma)
            transform_backward = "((x)**%f)" % (1. / abs(gamma))
    else:
        transform_forward = configs[conf]['transform_forward']
        transform_backward = configs[conf]['transform_backward']

  pidmin = 0.
  pidmax = 1.
  if 'limits' in configs[conf]:
    pidmin = configs[conf]['limits'][0]
    pidmax = configs[conf]['limits'][1]
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

  print(transform_backward)

  ranges = [
    (pidmin, pidmax), 
    (5.5, 9.5), 
    (1.5, 5.5), 
    (3.0, 6.5)
  ]

  counts, edges = get_template(datapdf, 4*[(0., 1.)])
  counts_mc, edges_mc = get_template(simpdf, 4*[(0., 1.)])

  print(transform_forward)
  print(transform_backward)
  
  print(counts.shape)
  print(counts_mc.shape)

  transform_forward_func = eval("lambda x : (" + transform_forward + ")")

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

  branches = [oldpidvar, ptvar, etavar, ntrvar]

  data = uproot.concatenate(infilename, expressions = branches)
  input_data = np.stack([data[oldpidvar].to_numpy(), data[ptvar].to_numpy(), data[etavar].to_numpy(), data[ntrvar].to_numpy()*1.0 ], axis = 1)

  template = (counts, edges, [(None, ranges[0]), (None, ranges[1]), (None, ranges[2]), (None, ranges[3])])
  mc_template = (counts_mc, edges, [(None, ranges[0]), (None, ranges[1]), (None, ranges[2]), (None, ranges[3])])

  np.savez("smooth_pidcorr_data.npz", counts, allow_pickle = True)
  np.savez("smooth_pidcorr_mc.npz", counts_mc, allow_pickle = True)

  vardef = {
    "normalise_method" : "scale", 
    "transform_backward" : transform_backward,
    "data_range" : ranges[0], 
    "normalise_range" : (0., 1.), 
    "resample_bins" : 200, 
  }

  kine_data = data_transform(input_data[:,1:], config, scale = scale_list )
  pid_data = transform_forward_func(input_data[:,0])[:,np.newaxis]
  data = np.concatenate([pid_data, kine_data], axis=1)

  pid_arr, calib_stat, mc_stat = correct_data(data, config, vardef, template, mc_template, verbose = True)

  if not (nan is None) : 
    pid_arr = np.nan_to_num(pid_arr, nan = nan)

  output_arrays = [ pid_arr, calib_stat, mc_stat ]
  output_branches = [ pidvar, stat, mcstat ]

  if not friend : 
    write_array(outfilename, np.concatenate(output_arrays, axis = 1),
            branches = output_branches, input = infilename, tree = outtree, 
            step_size = step_size, library = library)
  else : 
    write_friend_array(outfilename, np.concatenate(output_arrays, axis = 1), 
            branches = output_branches, tree = outtree )

#legacy_correct("../../pidgen2_tests/edoardo/merged.root", outfilename = "out.root")
legacy_correct("../../pidgen2_tests/francesca/filtered.root", outfilename = "out.root", )
