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

import uproot
from scipy.ndimage import gaussian_filter
import numpy as np
import awkward as ak

from .tuples import write_array, write_friend_array, read_array
from .resampling import calib_transform, data_transform, get_or_create_template, get_or_create_mc_template, resample_data, correct_data
from .resampling import get_samples, get_mc_samples, get_variables

def create_corrector(
    sample = None, 
    dataset = None, 
    variable = None, 
    simversion = None, 
    maxfiles = 0, 
    usecache = False, 
    plot = False, 
    interactive = False, 
    kernel = None, 
    verbose = False, 
    local_storage = "./templates/", 
    global_storage = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/templates/", 
    local_mc_storage = "./mc_templates/", 
    global_mc_storage = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/mc_templates/", 
    cachedir = None, 
    nan = -1000., 
    scale = None, 
    filter_func = None
  ) : 

  config = get_samples()[sample][dataset]
  mc_config = get_mc_samples()[sample][f"{simversion}_{dataset}"]
  mc_variable = variable

  if "aliases" in config and variable in config["aliases"] : 
    aliased_variable = config["aliases"][variable]
    if verbose >= 0 : 
      print(f"Using alias '{aliased_variable}' for variable name '{variable}' in dataset '{dataset}', sample '{sample}'")
    variable = aliased_variable

  if "aliases" in mc_config and variable in mc_config["aliases"] : 
    aliased_variable = mc_config["aliases"][variable]
    if verbose >= 0 : 
      print(f"Using alias '{aliased_variable}' for variable name '{variable}' in MC dataset '{simversion}_{dataset}', sample '{sample}'")
    mc_variable = aliased_variable

  vardef = get_variables()[variable]
  mc_vardef = get_variables()[mc_variable]

  pp = pprint.PrettyPrinter(indent = 4)

  if verbose >= 1 : 
    print(f"Calibration sample config: {pp.pformat(config)}")
    print(f"MC sample config: {pp.pformat(mc_config)}")
    print(f"Variable definition: {pp.pformat(vardef)}")

  if verbose >= 0 :
    print(f"Checking if data template exists in the storage")

  # Create PID resampling template based on calibration sample
  counts, counts2, edges, normaliser = get_or_create_template(sample, dataset, variable, 
                             vardef, config, 
                             use_calib_cache = usecache, max_files = maxfiles, 
                             interactive_plots = interactive, 
                             control_plots = plot, verbose = verbose, 
                             local_prefix = local_storage, 
                             global_prefix = global_storage, 
                             cachedir = cachedir)

  mc_counts, mc_counts2, mc_edges, mc_normaliser = get_or_create_mc_template(simversion, 
                             sample, dataset, mc_variable, 
                             mc_vardef, mc_config, 
                             use_calib_cache = usecache, 
                             interactive_plots = interactive, 
                             control_plots = plot, verbose = verbose, 
                             local_prefix = local_mc_storage, 
                             global_prefix = global_mc_storage, 
                             cachedir = cachedir, 
                             external_normaliser = normaliser)

  # Evaluate scaling list if it is a string
  if isinstance(scale, str) : 
    scale_list = eval(scale)
  else : 
    scale_list = scale

  transform_forward = eval("lambda x : (" + vardef["transform_forward"] + ")")

  def smooth_templates(kernel) : 

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
      sampled_mc_counts = np.random.normal(mc_counts, mc_counts2)
    else : 
      sampled_counts = counts
      sampled_mc_counts = mc_counts

    if filter_func is None : 

      if verbose >= 0 :
        print(f"Applying Gaussian smearing with kernel {template_sigma}")

      smooth_counts = gaussian_filter(sampled_counts, template_sigma)
      smooth_mc_counts = gaussian_filter(sampled_mc_counts, template_sigma)

    else : 

      if verbose >= 0 :
        print(f"Applying custom filter with kernel {template_sigma}")

      smooth_counts = filter_func(sampled_counts, template_sigma)
      smooth_mc_counts = filter_func(sampled_mc_counts, template_sigma)

    template = smooth_counts, edges, normaliser
    mc_template = smooth_mc_counts, edges, normaliser

    return template, mc_template

  if kernel is not None : 
    template, mc_template = smooth_templates(kernel)
  else : 
    template = None
    mc_template = None

  print(template, mc_template)

  def corrector(input_data, kernel = None) : 
  
    if kernel is not None : 
      local_template, local_mc_template = smooth_templates(kernel)
    else : 
      if template is None or mc_template is None : 
        print("Define kernel either in `create_corrector` or in corrector call.")
        return 
      local_template, local_mc_template = template, mc_template

    kine_data = data_transform(input_data[:,1:], config, scale = scale_list )
    pid_data = transform_forward(input_data[:,0])[:,np.newaxis]
    data = np.concatenate([pid_data, kine_data], axis=1)

    pid_arr, calib_stat, mc_stat = correct_data(data, 
             config, vardef, local_template, local_mc_template, 
             verbose = verbose)

    if nan is not None : 
      pid_arr = np.nan_to_num(pid_arr, nan = nan)

    return pid_arr, calib_stat, mc_stat
  
  return corrector
    
