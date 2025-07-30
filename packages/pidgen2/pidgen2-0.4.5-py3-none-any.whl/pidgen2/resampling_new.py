##############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

"""
Functions for PID resampling of calibration data. 
"""

import importlib
import os
import sys
from itertools import product
from copy import deepcopy, copy
from hashlib import sha1
import json

from jax import numpy as np
import numpy as onp
import matplotlib
import matplotlib.pyplot as plt
import uproot
#import uproot3
from scipy.ndimage import gaussian_filter

from .plotting import plot, plot_distr2d, plot_distr1d, set_lhcb_style, plot_hist2d, plot_hist1d
from .tuples import read_array_filtered, write_array, read_array
from . import density_estimation as de

def truncate_middle(s, n):
  """
    Truncate the middle of a string to fit in maximum width, with ellipsis "...". 
    Helper function for debug output. 
      s : input string
      n : maximum width
    Returns: truncated string
  """
  if len(s) <= n : return s
  n_2 = int(n) // 2 - 3
  n_1 = n - n_2 - 3
  return '{0}...{1}'.format(s[:n_1], s[-n_2:])

def get_samples() :
  """
  Import all modules with calibration samples from the "samples" subdir
  and construct the dictionary of all calibration samples

  Returns: 
      Dictionary of all samples loaded from "samples/" subdirectory
  """
  from . import samples
  d = {}
  for i in samples.__all__ : 
    module = importlib.import_module("." + i, "pidgen2.samples")
    s = getattr(module, "sample")
    d[i] = s
  return d

def get_mc_samples() :
  """
  Import all modules with MC samples from the "samples" subdir
  and construct the dictionary of all MC samples

  Returns: 
      Dictionary of all MC samples loaded from "samples/" subdirectory
  """
  from . import samples
  d = {}
  for i in samples.__all__ : 
    module = importlib.import_module("." + i, "pidgen2.samples")
    if hasattr(module, "mc_sample") : 
      s = getattr(module, "mc_sample")
      d[i] = s
  return d

def get_variables() : 
  """
  Import all modules with variables description from the "variables" subdir
  and construct the dictionary of all variables. 

  Returns: 
      Dictionary of all variables loaded from "variables/" subdirectory
  """
  from . import variables
  d = {}
  for i in variables.__all__ : 
    module = importlib.import_module("." + i, "pidgen2.variables")
    c = getattr(module, "variable")
    d[i] = c
  return d

def read_calib_tuple(sample, trees, expressions, branches, verbose = False, cachedir = None, cut = None) : 
  """ 
  Read calibration sample from the list of files into numpy array. 

  Args: 
    sample: tuple in the form (formatstring, numfiles) describing the calibration sample.
    trees: list of ROOT trees to read from the calibration files 
    branches: list of branches to read. 
    cachedir: If not None, store the copy of each input tree into the local cache file 
              under cachedir (only the selected branches)

  Returns: 
    2D numpy array, result of concatenation of all calibration samples. 
    The 1st index of 2D array corresponds to event, 2nd index to the variable from the branches list. 
  """
  datasets = []
  if cachedir : 
    os.system(f"mkdir -p {cachedir}")
  for i,filename in enumerate(sample) : 

    sys.stdout.write(f"\rReading file ({i+1}/{len(sample)}) {truncate_middle(filename, 80)}")
    sys.stdout.flush()

    if cachedir : 
      calib_cache_filename = cachedir + "/" + filename.split("/")[-1]
      file = uproot.recreate(calib_cache_filename, compression=uproot.ZLIB(4))

    for tree in trees : 
      try : 
        for t in uproot.iterate(filename + ":" + tree, library = "pd", expressions = branches, cut = cut) :

          arr = np.stack([ t.eval(b).values for b in expressions ], axis = 1)

          if cachedir : 
            outtree = tree.replace("/", "_") # Subdirs are not supported by uproot
            file[outtree] = { b : arr[:,i] for i,b in enumerate(expressions) }

          #if verbose : print(f"Reading tree {tree}, {arr.shape[0]} events")
          datasets += [ arr ]

      except FileNotFoundError : 
        print(f"... file not found, skipping")
        break

      except OSError : 
        print(f"... XRootD error reading calibration file {filename}. Please check your Kerberos ticket and try again. ")
        raise SystemExit

    if cachedir : 
      file.close()

  print("")

  if len(datasets) == 0 : 
    print(f"No input calibration files found. Do you have a valid Kerberos ticket to access EOS?")
    print(f"Will not create PID template, exiting...\n\n")
    raise SystemExit

  return datasets

def read_calib_file(filename, trees, expressions, branches, cachedir = None, cut = None, cache_action = None) : 
  """ 
  Read calibration sample from the calibration file into numpy array. 

  Args: 
    filename: calibration ROOT file name
    trees: list of ROOT trees to read from the calibration files 
    branches: list of branches to read. 
    cachedir: If not None, store the copy of each input tree into the local cache file 
              under cachedir (only the selected branches)

  Returns: 
    2D numpy array, result of concatenation of calibration branches. 
    The 1st index of 2D array corresponds to event, 2nd index to the variable from the branches list. 
  """
  datasets = []
  if cachedir : 
    cache_filename = cachedir + "/" + filename.split("/")[-1]
    if cache_action == "store" : 
      os.system(f"mkdir -p {cachedir}")
      file = uproot.recreate(cache_filename, compression=uproot.ZLIB(4))

  # Make branches a list of lists, if not. 
  if not isinstance(branches[0], list) : 
    branches = [ branches ]
    cut = [ cut ]
    expressions = [ expressions ]

  for tree in trees : 
    cache_tree = tree.replace("/", "_") # Subdirs are not supported by uproot
    if cache_action != "read" or cachedir is None : 
      try : 
        #print(f"Branches = {branches}, expressions = {expressions}, file = {filename}, tree = {tree}")
        for br,c,expr in zip(branches, cut, expressions) : 
          for t in uproot.iterate(filename + ":" + tree, library = "pd", expressions = br, cut = c) :
            arr = np.stack([ t.eval(b).values for b in expr ], axis = 1)
            if cachedir : file[cache_tree] = { b : arr[:,i] for i,b in enumerate(expr) }
            datasets += [ arr ]

      except FileNotFoundError : 
        print(f"\n... file not found, skipping")
        break

      except OSError : 
        print(f"\n... XRootD error reading calibration file {filename}. Please check your Kerberos ticket and try again. ")
        raise SystemExit

    else : 
      try : 
        with uproot.open(cache_filename + ":" + cache_tree) as t : 
          arr = t.arrays(expressions, library = "pd")[expressions].to_numpy()
          datasets += [ arr ]

      except FileNotFoundError : 
        print(f"\n... cached file not found, skipping")
        break

  if cachedir and cache_action == "store" : file.close()

  if len(datasets)>0 : 
    return np.concatenate(datasets, axis = 0)
  else : 
    if cachedir and cache_action == "store" :
      os.system(f"rm -f {cache_filename}")
    return None


def read_calib_cache(cachedir, sample, trees, branches, verbose = False) : 
  """ 
  Read cached calibration sample from the list of files into numpy array. 

  Args: 
    cachedir: local cache directory
    sample: tuple in the form (formatstring, numfiles) describing the calibration sample.
    trees: list of ROOT trees to read from the calibration files 
    branches: list of branches to read. 

  Returns: 
    2D numpy array, result of concatenation of all calibration samples. 
    The 1st index of 2D array corresponds to event, 2nd index to the variable from the branches list. 
  """
  datasets = []
  
  for i,filename in enumerate(sample) : 

    calib_cache_filename = cachedir + "/" + filename.split("/")[-1]

    sys.stdout.write(f"\rReading cached file ({i+1}/{len(sample)}) {truncate_middle(calib_cache_filename, 80)}")
    sys.stdout.flush()

    for tree in trees : 

      treename = tree.replace("/", "_") # Subdirs are not supported by uproot in cache files

      with uproot.open(calib_cache_filename + ":" + treename) as t :
        arr = t.arrays(branches, library = "pd")[branches].to_numpy()
        datasets += [ arr ]

  print("")

  if len(datasets) == 0 : 
    print(f"No input cache files found.")
    print(f"Will not create PID template, exiting...\n\n")
    raise SystemExit

  return datasets

def calib_transform(x, config, variable) :
  """
  Apply variable transformation to the calibration array. 

  Args: 
    x: 2D numpy array in the format returned by read_calib_tuple function. 
    config: calibration sample configuration dictionary. 
    variable: variable definition dictionary. 
  """

  transform_forward = eval("lambda x : (" + variable["transform_forward"] + ")")
  transform_sample = []
  for c in config["transform"] : 
    transform_sample += [ eval("lambda x : (" + c + ")") ]

  arr = [ transform_forward(x[:,0]) ]    # PID variable
  for i,(s,t) in enumerate(zip(config["smear"], transform_sample)) : 
    # If "smear" not None, do uniform random smearing before transformation
    if s : 
      xs = x[:,i+1] + s[0] + (s[1]-s[0])*onp.random.uniform(size = x.shape[0])
    else : 
      xs = x[:,i+1]
    arr += [ t(xs) ]
  arr += [ x[:,-1] ] # sWeight

  return np.stack(arr, axis = 1)

def data_transform(x, config, scale = None) :
  """
  Apply variable transformation to the data array. 

  Args: 
    x: 2D numpy array in the format returned by read_array function. 
    config: calibration sample configuration dictionary. 
    scale: optional vector of scale factors applied before transformation
           to each dimension of input data (e.g. to rescale multiplicity). 
  """
  transform_sample = [ ]
  for c in config["transform"] : 
    transform_sample += [ eval(f"lambda x : (" + c + ")") ]

  if scale : 
    arr = [ t(x[:,i]*s) for i, (t,s) in enumerate(zip(transform_sample, scale)) ]
  else : 
    arr = [ t(x[:,i]) for i, t in enumerate(transform_sample) ]

  return np.stack(arr, axis = 1)

def store_to_cache(variable, config, max_files = 0, verbose = False, cachedir = None) : 
  """
  Store selected branches from PID calibration samples to local cache files. 

  Args: 
    variable: variable definition dictionary.
    config: calibration sample configuration dictionary.
    max_files: Maximum number of calibration files to load (0 for unlimited)

  """
  sample = config['sample']
  trees = config['trees']
  expressions = [variable["expression"]] + config["branches"]
  if "branches" in variable :
    calib_branches = variable["branches"] + config["branches"]
  else : 
    calib_branches = expressions

  calib_cache_dirname = cachedir

  var_cut = variable.get("cut", None)
  sample_cut = config.get("cut", None)
  cut = var_cut
  if sample_cut:
    if cut : cut = f"({cut}) & ({sample_cut})"
    else : cut = sample_cut

  if verbose: 
    print(f"Cut: {cut}")

  if max_files == 0 : 
    raw_data = read_calib_tuple(sample, trees, expressions, calib_branches, verbose = verbose, cachedir = calib_cache_dirname, cut = cut)
  else : 
    raw_data = read_calib_tuple(sample[:max_files], trees, expressions, calib_branches, verbose = verbose, cachedir = calib_cache_dirname, cut = cut)
  print(f"Read {len(raw_data)} calibration subsamples from remote storage.")

def get_hash_config(sample_name, dataset_name, variable_name, variable, config, max_files, mc = False) : 
  hash_config = {
    "variable"  : deepcopy(variable), 
    "config"    : deepcopy(config), 
    "max_files" : max_files, 
  }

  # Remove keys that raw (unsmeared) template does not depend on
  config_keys_to_ignore = ["labels", "template_sigma", "variables"]
  variable_keys_to_ignore = ["template_sigma"]
  if not mc : variable_keys_to_ignore += ["mc_expression"]

  for k in config_keys_to_ignore : 
    if k in hash_config["config"] : hash_config["config"].pop(k)
  for k in variable_keys_to_ignore : 
    if k in hash_config["variable"] : hash_config["variable"].pop(k)
  return hash_config

def get_or_create_template(sample_name, dataset_name, variable_name, 
                    variable, config, kernels = None, use_calib_cache = False, control_plots = False, 
                    interactive_plots = False, local_prefix = ".", global_prefix = None, 
                    max_files = 0, verbose = False, cachedir = None) : 
  """

  """
  hash_config = get_hash_config(sample_name, dataset_name, variable_name, variable, config, max_files)
  config_hash = sha1(str(hash_config).encode('utf-8')).hexdigest()

  print(f"Template configuration hash : {config_hash}")

  if cachedir is None : 
    calib_cache_dirname = None 
  else : 
    calib_cache_dirname = f"{cachedir}/{sample_name}/{dataset_name}/{variable_name}/"

  template = None

  if global_prefix is not None : 
    template_storage = f"{global_prefix}/{sample_name}/{dataset_name}/{variable_name}/{config_hash}/"
    try: 

      #f = open(template_storage + "/config.json")
      #f.close()
      #data = onp.load(template_storage + "/template.npz", allow_pickle = True)
      #template = data["arr_0"], data["arr_1"], data["arr_2"], data["arr_3"]
      template = load_template(template_storage + "/template.root")

      print(f"Read template from {truncate_middle(template_storage, 80)}")

    except FileNotFoundError : 

      print(f"Template in global storage {template_storage} not found, will try local storage.")
      
  else : 
    print("Global storage location is None, will not be used")

  if template == None and local_prefix is not None : 

    template_storage = f"{local_prefix}/{sample_name}/{dataset_name}/{variable_name}/{config_hash}/"
    try : 

      template = load_template(template_storage + "/template.root")
      print(f"Read template from {truncate_middle(template_storage, 80)}")

    except FileNotFoundError : 

      print(f"Template in local storage {truncate_middle(template_storage, 80)} not found, will create one. Be patient...")

  else : 
    if local_prefix == None : 
      print("Local storage location is None, will not be used")
      template_storage = None

  if template == None : 

    print("Template will be created, be patient...")
    
    if template_storage : 
      os.system(f"mkdir -p {template_storage}")
    if (not use_calib_cache) and calib_cache_dirname : 
      os.system(f"mkdir -p {calib_cache_dirname}")

    template = create_template_multipass(variable, config, kernels = kernels, use_calib_cache = use_calib_cache, 
                    control_plots = control_plots, interactive_plots = interactive_plots, 
                    prefix = template_storage, max_files = max_files, verbose = verbose, cachedir = calib_cache_dirname)

    if template_storage : 
      f = open(template_storage + "/config.json", "w")
      json.dump(hash_config, f, indent = 4)
      f.close()
      #onp.savez_compressed(template_storage + "/template.npz", template[0], template[1], template[2], template[3] )
      save_template(template_storage + "/template.root", template)

  return template

def get_or_create_mc_template(sim_version, sample_name, dataset_name, variable_name, 
                    variable, config, kernels = None, use_calib_cache = False, control_plots = False, 
                    interactive_plots = False, local_prefix = ".", global_prefix = None, 
                    max_files = 0, verbose = False, cachedir = None, external_normaliser = None) : 
  """

  """
  hash_config = get_hash_config(sample_name, dataset_name, variable_name, variable, config, max_files, mc = True)
  config_hash = sha1(str(hash_config).encode('utf-8')).hexdigest()

  print(f"MC template configuration hash : {config_hash}")

  if cachedir is None : 
    calib_cache_dirname = None 
  else : 
    calib_cache_dirname = f"{cachedir}/{sim_version}/{sample_name}/{dataset_name}/{variable_name}/"

  template = None 

  if global_prefix is not None : 
    template_storage = f"{global_prefix}/{sim_version}/{sample_name}/{dataset_name}/{variable_name}/{config_hash}/"

    try: 
      template = load_template(template_storage + "/template.root")
      print(f"Read MC template from {truncate_middle(template_storage, 80)}")

    except FileNotFoundError : 
      print(f"MC template in global storage {template_storage} not found, will try local storage.")

  else : 
    print("Global MC storage location is None, will not be used")

  if template == None and local_prefix is not None : 

    template_storage = f"{local_prefix}/{sim_version}/{sample_name}/{dataset_name}/{variable_name}/{config_hash}/"

    try : 
      template = load_template(template_storage + "/template.root")
      print(f"Read MC template from {truncate_middle(template_storage, 80)}")

    except FileNotFoundError : 

      print(f"MC Template in local storage {truncate_middle(template_storage, 80)} not found, will create one. Be patient... ")

  else : 

    if local_prefix == None : 
      print("Local MC storage location is None, will not be used")
      template_storage = None

  if template == None : 

    print("MC template will be created, be patient...")

    if template_storage : 
      os.system(f"mkdir -p {template_storage}")
    if (not use_calib_cache) and calib_cache_dirname : 
      os.system(f"mkdir -p {calib_cache_dirname}")

    template = create_template_multipass(variable, config, kernels = kernels, use_calib_cache = use_calib_cache, 
                    control_plots = control_plots, interactive_plots = interactive_plots, 
                    prefix = template_storage, max_files = max_files, verbose = verbose, cachedir = calib_cache_dirname, mc = True, 
                    external_normaliser = external_normaliser)

    if template_storage : 
      f = open(template_storage + "/config.json", "w")
      json.dump(hash_config, f, indent = 4)
      f.close()

      save_template(template_storage + "/template.root", template)

  return template


def create_template(variable, config, kernels = None, use_calib_cache = False, control_plots = False, 
                    interactive_plots = False, prefix = "", max_files = 0, verbose = False, cachedir = None, 
                    external_normaliser = None) : 
  """
  Create PID calibration template from the calibration sample (smoothed PDF). 

  Args: 
    variable: variable definition dictionary.
    config: calibration sample configuration dictionary.
    kernels: optional list of kernel widths (if None, taken from config and variable definition dicts). 
    use_calib_cache: if True, take calibration sample from the local cache. 
    control_plots: if True, produce control plots (1D and 2D projections of calibration and smoothed distributions). 
    interactive_plots: if True, open control plots in interactive mode, if False, only store them to files. 
    prefix: prefix for control plots (e.g. --prefix="subdir/"). 
    max_files: Maximum number of calibration files to load (0 for unlimited)

  Returns: 
    template structure to be used for resampling. 
  """
  sample = config['sample']
  trees = config['trees']
  expressions = [variable["expression"]] + config["branches"]
  if "branches" in variable :
    calib_branches = variable["branches"] + config["branches"]
  else : 
    calib_branches = expressions
  ranges = [ variable["data_range"]] + config["data_ranges"]
  calib_cache_branches = ["pid"] + config["calib_cache_branches"]
  normalise_bins = [variable["normalise_bins"]] + config["normalise_bins"]
  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  template_bins = [variable["template_bins"]] + config["template_bins"]
  if kernels : 
    template_sigma = kernels
  else : 
    template_sigma = [variable["template_sigma"]["default"]] + config["template_sigma"]["default"]
  max_weights = config["max_weights"]

  onp.random.seed(1)  # To make variable transformation of the calibration sample (calib_transform) deterministic

  if use_calib_cache : 
    if max_files == 0 : 
      data = read_calib_cache(cachedir, sample, trees, expressions, verbose = verbose)
    else : 
      data = read_calib_cache(cachedir, sample[:max_files], trees, expressions, verbose = verbose)
    print(f"Read {len(data)} calibration subsamples from local cache.")
  else :

    var_cut = variable.get("cut", None)
    sample_cut = config.get("cut", None)
    cut = var_cut
    if sample_cut:
      if cut : cut = f"({cut}) & ({sample_cut})"
      else : cut = sample_cut

    if max_files == 0 : 
      data = read_calib_tuple(sample, trees, expressions, calib_branches, verbose = verbose, cachedir = cachedir, cut = cut)
    else : 
      data = read_calib_tuple(sample[:max_files], trees, expressions, calib_branches, verbose = verbose, cachedir = cachedir, cut = cut)

    #print(data)
    print(f"Read {len(data)} calibration subsamples from remote storage.")

  if (verbose) : print(f"Original data array: {data[0]}")

  if (verbose) : print(f"Starting to transform data array")
  for i, d in enumerate(data) : 
    d1 = calib_transform(d, config, variable)
    data[i] = d1
  if (verbose) : print(f"Transformed data array: {data[0]}")

  print(f"Starting to filter data, ranges = {ranges}")
  for i, d in enumerate(data) : 
    d1 = de.filter_data(d, ranges + [ (-1000., 1000.) ] )
    data[i] = d1
  if (verbose) : print(f"Filtered data: {data[0]}")

  weights1 = [ d[:,-1] for d in data ]

  weights = []
  if max_weights : 
    print(f"Starting to calculate flattening weights")
    histograms = de.create_histograms_vector(data, ranges = ranges, bins = normalise_bins, weights = weights1)[1:]
    for d,w in zip(data, weights1) : 
      weights2 = de.reweight(d[:,1:-1], histograms, max_weights = max_weights, weights = w)
      weights += [ weights2 ]
    if (verbose) : print(f"Weights vector: {weights[0]}")
  else : 
    weights = weights1

  if external_normaliser is not None : 
    print(f"Using external normaliser")
    normaliser = external_normaliser
  else : 
    print(f"Creating normaliser structure")
    normaliser = de.create_normaliser_vector(data, ranges = ranges, bins = normalise_bins, weights = weights)

  print(f"Starting to normalise data array")
  norm_data = []
  for d in data : 
    norm_data += [ de.normalise(d[:,:-1], normaliser, normalise_methods) ]
  if (verbose) : print(f"Normalised data array: {norm_data[0]}")

  #unnorm_data = de.unnormalise(norm_data, normaliser, normalise_methods)

  counts = None
  counts2 = None
  edges = None
  for i,(nd,w) in enumerate(zip(norm_data, weights)) : 
    sys.stdout.write(f"\rFilling histogram for subsample {i+1}/{len(norm_data)}")
    sys.stdout.flush()
    c, e = np.histogramdd(nd, bins = template_bins, range = normalise_ranges, weights = w)
    c2, e2 = np.histogramdd(nd, bins = template_bins, range = normalise_ranges, weights = w**2)
    if counts is None : 
      counts = c
      counts2 = c2
      edges = e
    else : 
      counts += c
      counts2 += c2

  print("")

  if control_plots : 

    print(f"Producing control plots")

    print(f"Applying default Gaussian smearing")
    smooth_counts = gaussian_filter(counts, template_sigma)

    labels = config["labels"]
    names = config["names"]

    log = True

    set_lhcb_style(size = 12, usetex = False)
    #fig, axes = plt.subplots(nrows = 7, ncols = 6, figsize = (12, 9) )

    for i in range(len(ranges)) : 

      if verbose : print(f"Plots for 1D projection {names[i]}")

      with plot(f"{names[i]}_transformed", prefix) as (fig, ax) : 
        plot_distr1d(data, i, bins = 50, range = ranges[i], ax = ax, label = "Transformed " + labels[i], weights = weights1, title = "Transformed distribution")

      with plot(f"{names[i]}_weighted", prefix) as (fig, ax) : 
        plot_distr1d(data, i, bins = 50, range = ranges[i], ax = ax, label = "Weighted " + labels[i], weights = weights, title = "Weighted distribution")

      with plot(f"{names[i]}_normalised", prefix) as (fig, ax) : 
        plot_distr1d(norm_data, i, bins = 50, range = normalise_ranges[i], ax = ax, label = "Normalised " + labels[i], weights = weights, title = "Normalised distribution")

    if len(ranges) == 3 : 

      smooth_proj = {
      (0, 1) : [np.sum(smooth_counts, 2), edges[0], edges[1]],
      (0, 2) : [np.sum(smooth_counts, 1), edges[0], edges[2]],
      (1, 2) : [np.sum(smooth_counts, 0), edges[1], edges[2]],
      }

      n1,n2,n3 = [int(n/2) for n in template_bins]  # Make slices through the central region of the distribution

      data_slices = {
      (0, 1) : [counts[:,:,n3], edges[0], edges[1]], 
      (0, 2) : [counts[:,n2,:], edges[0], edges[2]], 
      (1, 2) : [counts[n1,:,:], edges[1], edges[2]], 
      }

      smooth_slices = {
      (0, 1) : [smooth_counts[:,:,n3], edges[0], edges[1]], 
      (0, 2) : [smooth_counts[:,n2,:], edges[0], edges[2]], 
      (1, 2) : [smooth_counts[n1,:,:], edges[1], edges[2]], 
      }

    if len(ranges) == 4 : 

      smooth_proj = {
      (0, 1) : [np.sum(smooth_counts, (2,3)), edges[0], edges[1]],
      (0, 2) : [np.sum(smooth_counts, (1,3)), edges[0], edges[2]],
      (1, 2) : [np.sum(smooth_counts, (0,3)), edges[1], edges[2]],
      (0, 3) : [np.sum(smooth_counts, (1,2)), edges[0], edges[3]],
      (1, 3) : [np.sum(smooth_counts, (0,2)), edges[1], edges[3]],
      (2, 3) : [np.sum(smooth_counts, (0,1)), edges[2], edges[3]],
      }

      n1,n2,n3,n4 = [int(n/2) for n in template_bins]  # Make slices through the central region of the distribution

      data_slices = {
      (0, 1) : [counts[:,:,n3,n4], edges[0], edges[1]], 
      (0, 2) : [counts[:,n2,:,n4], edges[0], edges[2]], 
      (1, 2) : [counts[n1,:,:,n4], edges[1], edges[2]], 
      (0, 3) : [counts[:,n2,n3,:], edges[0], edges[3]], 
      (1, 3) : [counts[n1,:,n3,:], edges[1], edges[3]], 
      (2, 3) : [counts[n1,n2,:,:], edges[2], edges[3]], 
      }

      smooth_slices = {
      (0, 1) : [smooth_counts[:,:,n3,n4], edges[0], edges[1]], 
      (0, 2) : [smooth_counts[:,n2,:,n4], edges[0], edges[2]], 
      (1, 2) : [smooth_counts[n1,:,:,n4], edges[1], edges[2]], 
      (0, 3) : [smooth_counts[:,n2,n3,:], edges[0], edges[3]], 
      (1, 3) : [smooth_counts[n1,:,n3,:], edges[1], edges[3]], 
      (2, 3) : [smooth_counts[n1,n2,:,:], edges[2], edges[3]], 
      }

    for i,j in smooth_proj.keys() : 

      if verbose : print(f"Plots for 2D projection ({names[i]}, {names[j]})")

      with plot(f"{names[i]}_{names[j]}_data_proj", prefix) as (fig, ax) : 
        plot_distr2d(norm_data, i, j, bins = 2*[50], ranges = (normalise_ranges[i], normalise_ranges[j]), 
             fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), weights = weights, cmap = "jet", log = log, 
             title = "Data projection")

      with plot(f"{names[i]}_{names[j]}_smooth_proj", prefix) as (fig, ax) : 
        plot_hist2d(smooth_proj[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed projection")

      with plot(f"{names[i]}_{names[j]}_data_slice", prefix) as (fig, ax) : 
        plot_hist2d(data_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Data slice")

      with plot(f"{names[i]}_{names[j]}_smooth_slice", prefix) as (fig, ax) : 
        plot_hist2d(smooth_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed slice")

    #plt.tight_layout(pad=1., w_pad=1., h_pad=0.5)
    if interactive_plots : plt.show()

  return counts.astype(np.float32), np.sqrt(counts2).astype(np.float32), edges, normaliser

def create_template_multipass(variable, config, kernels = None, use_calib_cache = False, control_plots = False, 
                    interactive_plots = False, prefix = "", max_files = 0, verbose = False, cachedir = None, mc = False, 
                    external_normaliser = None) : 
  """
  Create PID calibration template from the calibration sample (smoothed PDF). 

  Args: 
    variable: variable definition dictionary.
    config: calibration sample configuration dictionary.
    kernels: optional list of kernel widths (if None, taken from config and variable definition dicts). 
    use_calib_cache: if True, take calibration sample from the local cache. 
    control_plots: if True, produce control plots (1D and 2D projections of calibration and smoothed distributions). 
    interactive_plots: if True, open control plots in interactive mode, if False, only store them to files. 
    prefix: prefix for control plots (e.g. --prefix="subdir/"). 
    max_files: Maximum number of calibration files to load (0 for unlimited)

  Returns: 
    template structure to be used for resampling. 
  """
  sample = config['sample']
  trees = config['trees']

  track_prefix = config.get("prefix")
  if not mc : 
    expressions = [variable["expression"].format(prefix = track_prefix)]
    if "branches" in variable :
      calib_branches = [ v.format(prefix = track_prefix) for v in variable["branches"]]
    else : 
      calib_branches = copy(expressions)
  else : 
    expressions = [variable["mc_expression"].format(prefix = track_prefix)]
    if "mc_branches" in variable :
      calib_branches = [ v.format(prefix = track_prefix) for v in variable["mc_branches"]]
    else : 
      calib_branches = copy(expressions)

  if "expressions" in config : 
    expressions += config["expressions"]
    calib_branches += config["branches"]
  else : 
    expressions += config["branches"]
    calib_branches += config["branches"]

  ranges = [ variable["data_range"]] + config["data_ranges"]
  calib_cache_branches = ["pid"] + config["calib_cache_branches"]
  normalise_bins = [variable["normalise_bins"]] + config["normalise_bins"]
  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  template_bins = [variable["template_bins"]] + config["template_bins"]
  if kernels : 
    template_sigma = kernels
  else : 
    template_sigma = [variable["template_sigma"]["default"]] + config["template_sigma"]["default"]
  max_weights = config["max_weights"]

  onp.random.seed(1)  # To make variable transformation of the calibration sample (calib_transform) deterministic

  if max_files != 0 : sample = sample[:max_files]

  var_cut = variable.get("cut", None)
  sample_cut = config.get("cut", None)
  cut = var_cut
  if sample_cut:
    if cut : cut = f"({cut}) & ({sample_cut})"
    else : cut = sample_cut
  
  if max_weights : 
    print(f"Pass: filling histograms for flattening weights")
    whistograms = None
    for i,filename in enumerate(sample) : 
      sys.stdout.write(f"Reading file ({i+1}/{len(sample)}) {truncate_middle(filename, 80)}\r")
      sys.stdout.flush()
      data = read_calib_file(filename, trees, expressions, calib_branches, cachedir = cachedir, cut = cut, cache_action = "store")
      if data is None : continue
      data = calib_transform(data, config, variable)
      data = de.filter_data(data, ranges + [ (-1000., 1000.) ] )
      whistograms = de.append_histograms(data, ranges = ranges, bins = normalise_bins, hists = whistograms, weights = data[:,-1])

    whistograms = whistograms[1:]  # Don't need the histogram for PID response itself

    if (verbose) : print(f"\nFlattening weight histograms: {whistograms}")

    print(f"\nPass: filling cumulative distributions for data preprocessing")
    histograms = None
    for i,filename in enumerate(sample) : 
      sys.stdout.write(f"\rReading file ({i+1}/{len(sample)}) {truncate_middle(filename, 80)}")
      sys.stdout.flush()
      data = read_calib_file(filename, trees, expressions, calib_branches, cachedir = cachedir, cut = cut, cache_action = "read")
      if data is None : continue
      data = calib_transform(data, config, variable)
      data = de.filter_data(data, ranges + [ (-1000., 1000.) ] )
      w = data[:,-1]
      w2 = de.reweight(data[:,1:-1], whistograms, max_weights = max_weights, weights = w)
 
      if (verbose) : print(f"\nFlattening weights: {w2/w}")
      histograms = de.append_histograms(data, ranges = ranges, bins = normalise_bins, hists = histograms, weights = w2)
  else : 
    print(f"\nPass: filling cumulative distributions for data preprocessing")
    histograms = None
    for i,filename in enumerate(sample) : 
      sys.stdout.write(f"\rReading file ({i+1}/{len(sample)}) {truncate_middle(filename, 80)}")
      sys.stdout.flush()
      data = read_calib_file(filename, trees, expressions, calib_branches, cachedir = cachedir, cut = cut, cache_action = "store")
      if data is None : continue
      data = calib_transform(data, config, variable)
      data = de.filter_data(data, ranges + [ (-1000., 1000.) ] )
      histograms = de.append_histograms(data, ranges = ranges, bins = normalise_bins, weights = data[:,-1])

  print(f"\nRead {len(sample)} calibration subsamples from remote storage.")

  if external_normaliser is not None : 
    print(f"Using external normaliser")
    normaliser = external_normaliser
  else : 
    print(f"Creating normaliser structure")
    normaliser = de.create_normaliser_from_histograms(histograms)

  print(f"Pass: filling resampling template")

  counts = None
  counts2 = None
  edges = None

  transformed_hists = len(ranges)*[ None ]
  weighted_hists = len(ranges)*[ None ]
  normalised_hists = len(ranges)*[ None ]

  for i,filename in enumerate(sample) : 
    sys.stdout.write(f"\rReading file ({i+1}/{len(sample)}) {truncate_middle(filename, 80)}")
    sys.stdout.flush()
    data0 = read_calib_file(filename, trees, expressions, calib_branches, cachedir = cachedir, cut = cut, cache_action = "read")
    if data0 is None : continue
    data = calib_transform(data0, config, variable)
    data = de.filter_data(data, ranges + [ (-1000., 1000.) ] )

    if (verbose) : print(f"\nFiltered data: {data}")

    if max_weights : 
      w1 = data[:,-1]
      w2 = de.reweight(data[:,1:-1], whistograms, max_weights = max_weights, weights = w1)
      w = w2
      if (verbose) : 
        print(f"sWeights: {w1}")
        print(f"Flattening weights: {w2}")
    else : 
      w = data[:,-1]

    norm_data = de.normalise(data[:,:-1], normaliser, normalise_methods)
    if (verbose) : print(f"Normalised data array: {norm_data}")

    c, e = np.histogramdd(norm_data, bins = template_bins, range = normalise_ranges, weights = w)
    c2, e2 = np.histogramdd(norm_data, bins = template_bins, range = normalise_ranges, weights = w**2)
    if counts is None : 
      counts = c
      counts2 = c2
      edges = e
    else : 
      counts += c
      counts2 += c2

    if control_plots : 
      for v in range(len(ranges)) : 
        c,e = np.histogram(data[:,v], bins = 50, range = ranges[v], weights = data[:,-1])
        if transformed_hists[v] is None : 
          transformed_hists[v] = [c, e]
        else : 
          transformed_hists[v][0] += c

        c,e = np.histogram(data[:,v], bins = 50, range = ranges[v], weights = w)
        if weighted_hists[v] is None : 
          weighted_hists[v] = [c, e]
        else : 
          weighted_hists[v][0] += c

        c,e = np.histogram(norm_data[:,v], bins = 50, range = normalise_ranges[v], weights = w)
        if normalised_hists[v] is None : 
          normalised_hists[v] = [c, e]
        else : 
          normalised_hists[v][0] += c          

  print("")

  if control_plots : 

    print(f"Producing control plots")

    print(f"Applying default Gaussian smearing")
    smooth_counts = gaussian_filter(counts, template_sigma)

    labels = config["labels"]
    names = config["names"]

    log = True

    set_lhcb_style(size = 12, usetex = False)
    #fig, axes = plt.subplots(nrows = 7, ncols = 6, figsize = (12, 9) )

    for i in range(len(ranges)) : 

      with plot(f"{names[i]}_transformed", prefix) as (fig, ax) : 
        plot_hist1d(transformed_hists[i], ax = ax, label = "Transformed " + labels[i], title = "Transformed distribution")

      with plot(f"{names[i]}_weighted", prefix) as (fig, ax) : 
        plot_hist1d(weighted_hists[i], ax = ax, label = "Weighted " + labels[i], title = "Weighted distribution")

      with plot(f"{names[i]}_normalised", prefix) as (fig, ax) : 
        plot_hist1d(normalised_hists[i], ax = ax, label = "Normalised " + labels[i], title = "Normalised distribution")

    if len(ranges) == 3 : 

      data_proj = {
      (0, 1) : [np.sum(counts, 2), edges[0], edges[1]],
      (0, 2) : [np.sum(counts, 1), edges[0], edges[2]],
      (1, 2) : [np.sum(counts, 0), edges[1], edges[2]],
      }

      smooth_proj = {
      (0, 1) : [np.sum(smooth_counts, 2), edges[0], edges[1]],
      (0, 2) : [np.sum(smooth_counts, 1), edges[0], edges[2]],
      (1, 2) : [np.sum(smooth_counts, 0), edges[1], edges[2]],
      }

      n1,n2,n3 = [int(n/2) for n in template_bins]  # Make slices through the central region of the distribution

      data_slices = {
      (0, 1) : [counts[:,:,n3], edges[0], edges[1]], 
      (0, 2) : [counts[:,n2,:], edges[0], edges[2]], 
      (1, 2) : [counts[n1,:,:], edges[1], edges[2]], 
      }

      smooth_slices = {
      (0, 1) : [smooth_counts[:,:,n3], edges[0], edges[1]], 
      (0, 2) : [smooth_counts[:,n2,:], edges[0], edges[2]], 
      (1, 2) : [smooth_counts[n1,:,:], edges[1], edges[2]], 
      }

    if len(ranges) == 4 : 

      data_proj = {
      (0, 1) : [np.sum(counts, (2,3)), edges[0], edges[1]],
      (0, 2) : [np.sum(counts, (1,3)), edges[0], edges[2]],
      (1, 2) : [np.sum(counts, (0,3)), edges[1], edges[2]],
      (0, 3) : [np.sum(counts, (1,2)), edges[0], edges[3]],
      (1, 3) : [np.sum(counts, (0,2)), edges[1], edges[3]],
      (2, 3) : [np.sum(counts, (0,1)), edges[2], edges[3]],
      }

      smooth_proj = {
      (0, 1) : [np.sum(smooth_counts, (2,3)), edges[0], edges[1]],
      (0, 2) : [np.sum(smooth_counts, (1,3)), edges[0], edges[2]],
      (1, 2) : [np.sum(smooth_counts, (0,3)), edges[1], edges[2]],
      (0, 3) : [np.sum(smooth_counts, (1,2)), edges[0], edges[3]],
      (1, 3) : [np.sum(smooth_counts, (0,2)), edges[1], edges[3]],
      (2, 3) : [np.sum(smooth_counts, (0,1)), edges[2], edges[3]],
      }

      n1,n2,n3,n4 = [int(n/2) for n in template_bins]  # Make slices through the central region of the distribution

      data_slices = {
      (0, 1) : [counts[:,:,n3,n4], edges[0], edges[1]], 
      (0, 2) : [counts[:,n2,:,n4], edges[0], edges[2]], 
      (1, 2) : [counts[n1,:,:,n4], edges[1], edges[2]], 
      (0, 3) : [counts[:,n2,n3,:], edges[0], edges[3]], 
      (1, 3) : [counts[n1,:,n3,:], edges[1], edges[3]], 
      (2, 3) : [counts[n1,n2,:,:], edges[2], edges[3]], 
      }

      smooth_slices = {
      (0, 1) : [smooth_counts[:,:,n3,n4], edges[0], edges[1]], 
      (0, 2) : [smooth_counts[:,n2,:,n4], edges[0], edges[2]], 
      (1, 2) : [smooth_counts[n1,:,:,n4], edges[1], edges[2]], 
      (0, 3) : [smooth_counts[:,n2,n3,:], edges[0], edges[3]], 
      (1, 3) : [smooth_counts[n1,:,n3,:], edges[1], edges[3]], 
      (2, 3) : [smooth_counts[n1,n2,:,:], edges[2], edges[3]], 
      }

    for i,j in smooth_proj.keys() : 

      if verbose : print(f"Plots for 2D projection ({names[i]}, {names[j]})")

      with plot(f"{names[i]}_{names[j]}_data_proj", prefix) as (fig, ax) : 
        plot_hist2d(data_proj[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Data projection")

      with plot(f"{names[i]}_{names[j]}_smooth_proj", prefix) as (fig, ax) : 
        plot_hist2d(smooth_proj[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed projection")

      with plot(f"{names[i]}_{names[j]}_data_slice", prefix) as (fig, ax) : 
        plot_hist2d(data_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Data slice")

      with plot(f"{names[i]}_{names[j]}_smooth_slice", prefix) as (fig, ax) : 
        plot_hist2d(smooth_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed slice")

    #plt.tight_layout(pad=1., w_pad=1., h_pad=0.5)
    if interactive_plots : plt.show()

  return counts.astype(np.float32), np.sqrt(counts2).astype(np.float32), edges, normaliser

def save_template(filename, template) : 
  """
    Save PID template into ROOT file 
    Args: 
      filename: output ROOT file name
      template: PID template (in the format as provided by e.g. create_template)
  """

  counts, counts2, edges, norm = template

  with uproot.recreate(filename, compression=uproot.ZLIB(4)) as of :

    of["counts_data"] = { "n"  : counts.flatten("F"), 
                          "n2" : counts2.flatten("F") }
    of["counts_shape"] = { "i" : counts.shape }

    for i,e in enumerate(edges) : 
      of[f"edges_{i}_data"] = { "n" : e }

    for i,(cnt, edg) in enumerate(norm) : 
      of[f"norm_cnt_{i}_data"] = { "n" : cnt }
      of[f"norm_edg_{i}_data"] = { "n" : edg }

def load_template(filename) : 
  """
    Load PID template from the ROOT file
    Args: 
      filename: Name of the ROOT file or its URL (opened via uproot)
    
    Returns: 
      PID template in the same format as provided by create_template
  """
  with uproot.open(filename) as f :
    counts_data = f["counts_data"]["n"].array(library = "np")
    counts_shape = f["counts_shape"]["i"].array(library = "np")
    counts2_data = f["counts_data"]["n2"].array(library = "np")

    counts = counts_data.reshape(counts_shape, order = "F")
    counts2 = counts2_data.reshape(counts_shape, order = "F")

    edges = []
    norm = []
    for i in range(len(counts.shape)) : 
      edges_data = f[f"edges_{i}_data"]["n"].array(library = "np")
      edges += [ edges_data ]
      norm_cnt_data = f[f"norm_cnt_{i}_data"]["n"].array(library = "np")
      norm_edg_data = f[f"norm_edg_{i}_data"]["n"].array(library = "np")
      norm += [ (norm_cnt_data, norm_edg_data) ]

    return counts, counts2, edges, norm


def resample_data(data, config, variable, template, chunk_size = 50000, verbose = False) : 
  """
  Perform resampling of data sample using the template created by create_template function.

  Args: 
    data: numpy 2D array with input data 
    config: calibration sample configuration dictionary.
    variable: variable definition dictionary.
    template: PID template structure.
    chunk_size: Size of data chunk for vectorised processing.

  Returns: 
    Tuple of (pid_arr, pid_stat), where
      pid_arr: numpy 1D array of resampled PID data. 
      pid_stat: numpy 1D array of effective template statistics per each event.
  """

  counts, edges, normaliser = template

  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  resample_bins = variable["resample_bins"]
  transform_backward = eval("lambda x : (" + variable["transform_backward"] + ")")

  norm_data = de.normalise(data, normaliser[1:], normalise_methods[1:])

  if (verbose) : 
    print(f"Normalised data: {norm_data[:100]}")

  start_index = 0
  chunk = 0
  resampled_pid_arrs = []
  pid_calib_stats = []
  stop = False
  chunks = (len(norm_data)-1)//chunk_size+1

  while not stop : 
    print(f"Resampling chunk {chunk+1}/{chunks}, index={start_index}/{len(norm_data)}")
    end_index = start_index + chunk_size
    if end_index >= len(norm_data) :
      end_index = len(norm_data)
      stop = True

    rnd = onp.random.uniform(size = (end_index-start_index, ))
    norm_pid, stats = de.resample(counts, edges, norm_data[start_index:end_index,], 
                          rnd = rnd, range = normalise_ranges[0], 
                          bins = resample_bins)
    unnorm_pid = de.unnormalise(norm_pid, normaliser[0:1], normalise_methods)
    resampled_pid = transform_backward(unnorm_pid)

    resampled_pid_arrs += [ resampled_pid ]
    pid_calib_stats += [ stats ]

    start_index += chunk_size
    chunk += 1

  resampled_pid_arr = np.concatenate(resampled_pid_arrs, axis = 0)
  pid_calib_stat = np.concatenate(pid_calib_stats, axis = 0)
  return resampled_pid_arr, pid_calib_stat

  #output_data = np.concatenate([data[start_index:end_index,:], norm_data[start_index:end_index,:], unnorm_data[:nev,:], 
  #                              norm_pid, unnorm_pid, resampled_pid], axis = 1)
  #write_array("output.root", output_data, branches = 
  #            ["pid", "pt", "eta", "ntr", "sw", 
  #             "normpid", "normpt", "normeta", "normntr", 
  #             "unnormpid", "unnormpt", "unnormeta", "unnormntr", 
  #             "normpidgen", "pidgen", "respidgen"])

def correct_data(data, config, variable, template, mc_template, chunk_size = 50000, verbose = False) : 
  """
  Perform correction of data sample using the data and mc templates created by create_template function.

  Args: 
    data: numpy 2D array with input data 
    config: calibration sample configuration dictionary.
    variable: variable definition dictionary.
    template: PID template structure.
    chunk_size: Size of data chunk for vectorised processing.

  Returns: 
    Tuple of (pid_arr, pid_stat), where
      pid_arr: numpy 1D array of resampled PID data. 
      pid_stat: numpy 1D array of effective template statistics per each event.
  """

  counts, edges, normaliser = template
  mc_counts, mc_edges, mc_normaliser = mc_template

  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  resample_bins = variable["resample_bins"]
  transform_backward = eval("lambda x : (" + variable["transform_backward"] + ")")

  norm_data = de.normalise(data, normaliser, normalise_methods)

  if (verbose) : 
    print(f"Normalised data: {norm_data[:100]}")

  start_index = 0
  chunk = 0
  pid_calib_stats = []
  pid_mc_stats = []
  corrected_pid_arrs = []
  stop = False
  chunks = (len(norm_data)-1)//chunk_size+1

  while not stop : 
    print(f"Correcting chunk {chunk+1}/{chunks}, index={start_index}/{len(norm_data)}")
    end_index = start_index + chunk_size
    if end_index >= len(norm_data) :
      end_index = len(norm_data)
      stop = True

    prob, mc_stats = de.probability(mc_counts, edges, norm_data[start_index:end_index,1:], 
                          norm_data[start_index:end_index,0], 
                          range = normalise_ranges[0], bins = resample_bins)

    #print(f"prob[{prob.shape}]={prob}")

    norm_pid, stats = de.resample(counts, edges, norm_data[start_index:end_index,1:], 
                          rnd = prob, range = normalise_ranges[0], 
                          bins = resample_bins)

    #print(f"norm_pid[{norm_pid.shape}]={norm_pid}")

    unnorm_pid = de.unnormalise(norm_pid, normaliser[0:1], normalise_methods[0:1])
    corrected_pid = transform_backward(unnorm_pid)

    #print(f"corrected_pid[{corrected_pid.shape}]={corrected_pid}")

    corrected_pid_arrs += [ corrected_pid ]
    pid_calib_stats += [ stats ]
    pid_mc_stats += [ mc_stats ]

    start_index += chunk_size
    chunk += 1

  corrected_pid_arr = np.concatenate(corrected_pid_arrs, axis = 0)
  pid_calib_stat = np.concatenate(pid_calib_stats, axis = 0)
  pid_mc_stat = np.concatenate(pid_mc_stats, axis = 0)
  return corrected_pid_arr, pid_calib_stat, pid_mc_stat
