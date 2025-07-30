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

import sys
import argparse
import pprint

from . import init

import numpy as np
import uproot
from scipy.ndimage import gaussian_filter

from .tuples import write_array, write_friend_array, read_array
from .resampling import calib_transform, data_transform, get_or_create_template, resample_data
from .resampling import get_samples, get_variables

def create_resampler(
    resampling_seed = 1000, 
    sample = None, 
    dataset = None, 
    variable = None, 
    maxfiles = 0, 
    usecache = False, 
    plot = False, 
    interactive = False, 
    kernel = None, 
    verbose = False, 
    local_storage = "/eos/lhcb/wg/PID/PIDGen2/templates/", 
    global_storage = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/templates/", 
    cachedir = None, 
    nan = -1000., 
    scale = None, 
    filter_func = None
  ) : 

  config = get_samples()[sample][dataset]
  pp = pprint.PrettyPrinter(indent = 4)

  if "aliases" in config and variable in config["aliases"] : 
    aliased_variable = config["aliases"][variable]
    print(f"Using alias '{aliased_variable}' for variable name '{variable}' in dataset '{dataset}', sample '{sample}'")
    variable = aliased_variable

  vardef = get_variables()[variable]

  if verbose >= 1 : 
    print(f"Calibration sample config: {pp.pformat(config)}")
    print(f"Variable definition: {pp.pformat(vardef)}")

  if verbose >= 0 : 
    print(f"Checking if template exists in the storage")

  # Create PID resampling template based on calibration sample
  counts, counts2, edges, normaliser = get_or_create_template(sample, dataset, variable, 
                             vardef, config, 
                             use_calib_cache = usecache, max_files = maxfiles, 
                             interactive_plots = interactive, 
                             control_plots = plot, verbose = verbose, 
                             local_prefix = local_storage, 
                             global_prefix = global_storage, 
                             cachedir = cachedir)

  # Evaluate scaling list if it is a string
  if isinstance(scale, str) : 
    scale_list = eval(scale)
  else : 
    scale_list = scale

  def smooth_template(kernel) : 

    if isinstance(kernel, (list, tuple)) : 
      kernel_name = kernel[0]
      template_seed = kernel[1]
    else : 
      kernel_name = kernel
      template_seed = None

    if isinstance(kernel_name, str) : 
      if kernel_name.find(",") > 0 : 
        template_sigma = eval(kernel_name)
      else : 
        template_sigma = [vardef["template_sigma"][kernel_name]] + config["template_sigma"][kernel_name]
    elif kernel_name is None : 
      template_sigma = [vardef["template_sigma"]["default"]] + config["template_sigma"]["default"]
    else : 
      template_sigma = kernel_name

    if not ((template_seed is None) or (template_seed == 0) ) : 
        if verbose >= 0 : 
          print(f"Random sampling of raw template with seed {template_seed}")
        np.random.seed(template_seed)
        sampled_counts = np.random.normal(counts, counts2)
    else : 
        sampled_counts = counts

    if filter_func is None : 

      if verbose >= 0 :
        print(f"Applying Gaussian smearing with kernel {template_sigma}")

      smooth_counts = gaussian_filter(sampled_counts, template_sigma)

    else : 

      if verbose >= 0 :
        print(f"Applying custom filter with kernel {template_sigma}")

      smooth_counts = filter_func(sampled_counts, template_sigma)

    template = smooth_counts, edges, normaliser
    
    return template

  if kernel is not None : 
    template = smooth_template(kernel)
  else : 
    template = None

  np.random.seed(resampling_seed)

  def resampler(input_data, kernel = None) : 
  
    if verbose >= 0 : 
      print(f"Running resampler")
      
    if kernel is not None : 
      local_template = smooth_template(kernel)
    else : 
      if template is None : 
        print("Define kernel either in `create_resampler` or in resampler call.")
        return 
      local_template = template

    data = data_transform(input_data, config, scale = scale_list )
    pid_arr, calib_stat = resample_data(data, config, vardef, local_template, verbose = verbose)

    if not (nan is None) : 
      pid_arr = np.nan_to_num(pid_arr, nan = nan)

    return pid_arr, calib_stat

  return resampler
