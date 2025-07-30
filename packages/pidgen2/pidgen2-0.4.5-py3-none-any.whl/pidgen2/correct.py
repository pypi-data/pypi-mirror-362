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

#from jax import numpy as np
#import numpy as onp
import uproot
from scipy.ndimage import gaussian_filter
import numpy as np
import awkward as ak

from .tuples import write_array, write_friend_array, read_array
from .resampling import calib_transform, data_transform, get_or_create_template, get_or_create_mc_template, resample_data, correct_data
from .resampling import get_samples, get_mc_samples, get_variables

def correct(
    input = None, 
    output = None, 
    outtree = "tree", 
    sample = None, 
    dataset = None, 
    variable = None, 
    simversion = None, 
    branches = "pt:eta:ntr", 
    pidcorr = "pidcorr", 
    stat = "pidstat", 
    mcstat = "pidmcstat", 
    maxfiles = 0, 
    start = None, 
    stop = None, 
    usecache = False, 
    plot = False, 
    interactive = False, 
    kernels = None, 
    verbose = False, 
    friend = False, 
    library = "ak", 
    step_size = 100000, 
    local_storage = "/eos/lhcb/wg/PID/PIDGen2/templates/", 
    global_storage = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/templates/", 
    local_mc_storage = "/eos/lhcb/wg/PID/PIDGen2/mc_templates/", 
    global_mc_storage = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/mc_templates/", 
    cachedir = None, 
    eta_from_p = False, 
    nan = -1000., 
    scale = None, 
    filter_func = None
  ) : 

  input_branches = branches.split(":") if isinstance(branches, str) else branches

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

  from numpy.lib.recfunctions import structured_to_unstructured as s2u
  input_df = uproot.concatenate(input, input_branches, library = "ak")
  input_data = s2u(input_df[input_branches]).to_numpy()
  
  start_event = start
  stop_event = stop

  if (stop_event is not None) and stop_event > len(input_data) : stop_event = len(input_data)
  else : input_data = input_data[start_event:stop_event]
  if verbose >= 1 : print (f"Shape of the array for resampling: {input_data.shape}")

  if eta_from_p : 
    # Replace momentum by eta calculated from p (index 1) and pT (index 2)
    input_data[:,2] = -np.log(np.tan(np.arcsin(input_data[:,1]/input_data[:,2])/2.))

  if not friend :
    if verbose >= 1 :
      all_branches = list(uproot.open(input).keys())
      print (f"List of all input tree branches: {pp.pformat(all_branches)}")

  # Loop over kernels
  kernel_list = kernels
  if not isinstance(kernels, (list, tuple)) : 
    kernel_list = [ kernels ]

  # Evaluate scaling list if it is a string
  if isinstance(scale, str) : 
    scale_list = eval(scale)
  else : 
    scale_list = scale

  output_arrays = []
  output_branches = []

  transform_forward = eval("lambda x : (" + vardef["transform_forward"] + ")")

  for kernel_num, kernel in enumerate(kernel_list) : 
    if isinstance(kernel, (list, tuple)) : 
      kernel_name = kernel[0]
      template_seeds = kernel[1]
    else : 
      kernel_name = kernel
      template_seeds = [ None ]

    if isinstance(kernel_name, str) : 
      if kernel_name.find(",") > 0 : 
        template_sigma = eval(kernel_name)
        kernel_name = f"kern{kernel_num}"
      else : 
        template_sigma = [vardef["template_sigma"][kernel_name]] + config["template_sigma"][kernel_name]
    elif kernel_name is None : 
      template_sigma = [vardef["template_sigma"]["default"]] + config["template_sigma"]["default"]
      kernel_name = "default"
    else : 
      template_sigma = kernel_name
      kernel_name = f"kern{kernel_num}"

    for template_seed in template_seeds : 

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
        #np.savez("smooth_pidgen2_data.npz", smooth_counts, allow_pickle = True)
        #np.savez("smooth_pidgen2_mc.npz", smooth_mc_counts, allow_pickle = True)

      template = smooth_counts, edges, normaliser
      mc_template = smooth_mc_counts, edges, normaliser  # or mc_normaliser? - no

      if verbose >= 0 :
        print(f"Smeared template ready, starting resampling")

      kine_data = data_transform(input_data[:,1:], config, scale = scale_list )
      pid_data = transform_forward(input_data[:,0])[:,np.newaxis]
      data = np.concatenate([pid_data, kine_data], axis=1)

      pid_arr, calib_stat, mc_stat = correct_data(data, config, vardef, template, mc_template, verbose = verbose)

      if not (nan is None) : 
        pid_arr = np.nan_to_num(pid_arr, nan = nan)

      output_arrays += [ pid_arr, calib_stat, mc_stat ]
      if (template_seed is None) or (template_seed == 0) : 
        output_branches += [ f"{pidcorr}_{kernel_name}", f"{stat}_{kernel_name}", f"{mcstat}_{kernel_name}" ]
      else : 
        output_branches += [ f"{pidcorr}_{kernel_name}_{template_seed}", f"{stat}_{kernel_name}_{template_seed}", f"{mcstat}_{kernel_name}_{template_seed}" ]

      if verbose >= 1 : 
        print(f"Input data array: {input_data[:100]}")
        print(f"Data array after variable transformation: {data[:100]}")
        print(f"Resampled PID array: {pid_arr[:100]}")
        print(f"Resampling statistics array: {calib_stat[:100]}")
        print(f"Resampling MC statistics array: {mc_stat[:100]}")

  # End of loop over kernels

  if not friend : 
    write_array(output, np.concatenate(output_arrays, axis = 1),
            branches = output_branches, input = input, tree = outtree, 
            step_size = step_size, library = library, verbose = verbose)
  else : 
    write_friend_array(output, np.concatenate(output_arrays, axis = 1), 
            branches = output_branches, tree = outtree )

def main() : 

  parser = argparse.ArgumentParser(description = "PIDGen2 correction script", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--input', type=str, default = None, 
                      help="Input ROOT path (file:tree), wildcards allowed")
  parser.add_argument('--output', type=str, default = None, 
                      help="Output ROOT file")
  parser.add_argument('--outtree', type=str, default = "tree", 
                      help="Output TTree")
  parser.add_argument('--sample', type=str, default = None, 
                      help="Calibration sample name")
  parser.add_argument('--simversion', type=str, default = None, 
                      help="Simulation version")
  parser.add_argument('--dataset', type=str, default = None, 
                      help="Calibration dataset in the form Polarity_Year, e.g. MagUp_2018")
  parser.add_argument('--variable', type=str, default = None, 
                      help="PID variable to resample")
  parser.add_argument('--branches', type=str, default = "pt:eta:ntr", 
                      help="Input branches for Pt,Eta,Ntracks variables in the form Pt:Eta:Ntrack")
  parser.add_argument('--pidcorr', type=str, default = "pidcorr", 
                      help="Corrected PID branch")
  parser.add_argument('--stat', type=str, default = "pidstat", 
                      help="PID calibration statistics branch")
  parser.add_argument('--mcstat', type=str, default = "pidmcstat", 
                      help="PID MC statistics branch")
  parser.add_argument('--maxfiles', type=int, default = 0, 
                      help="Maximum number of calibration files to read (0-unlimited)")
  parser.add_argument('--start', type=int, default = 0, 
                      help="Start event")
  parser.add_argument('--stop', type=int, default = -1, 
                      help="Stop event")
  parser.add_argument('--usecache', default = False, action = "store_const", const = True, 
                      help='Use calibration cache')
  parser.add_argument('--plot', default = False, action = "store_const", const = True, 
                      help='Produce control plots')
  parser.add_argument('--interactive', default = False, action = "store_const", const = True, 
                      help='Show control plots interactively')
  parser.add_argument('--kernels', type=str, default = None, 
                      help='Smearing kernel definition (e.g. --kernel="2,3,3,4" or --kernel="syst_1"), if None, use "default"')
  parser.add_argument('--verbose', default = False, action = "store_const", const = True, 
                      help='Enable debug messages')
  parser.add_argument('--friend', default = False, action = "store_const", const = True, 
                      help='Create friend tree with only resampled PID and statistics branches')
  parser.add_argument('--library', type=str, default = "ak", choices = ["ak", "np", "pd"], 
                      help='Library to handle ROOT ntuples with uproot')
  parser.add_argument('--step_size', type=int, default = 100000, 
                      help='Chunk size for ROOT file writing with uproot')
  parser.add_argument('--local_storage', type=str, default = "/eos/lhcb/wg/PID/PIDGen2/templates/", 
                      help="Local template storage directory")
  parser.add_argument('--global_storage', type=str, default = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/templates/", 
                      help="Global template storage directory")
  parser.add_argument('--local_mc_storage', type=str, default = "/eos/lhcb/wg/PID/PIDGen2/mc_templates/", 
                      help="Local template storage directory")
  parser.add_argument('--global_mc_storage', type=str, default = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/mc_templates/", 
                      help="Global template storage directory")
  parser.add_argument('--cachedir', type=str, default = None, 
                      help="Local calibration sample cache directory")
  parser.add_argument('--eta_from_p', default = False, action = "store_const", const = True, 
                      help='Calculate eta from p and pT branches')
  parser.add_argument('--nan', type=float, default = -1000., 
                      help="Numerical value to replace NaN in resampled PID (when calibration data is missing)")
  parser.add_argument('--scale', type=str, default = None, 
                      help="List of scale factors for input data e.g. --scale='1,1,1.15' for 15%% upscaling of multiplicity")

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  correct(**vars(args))

if __name__ == "__main__" : 
  main()
