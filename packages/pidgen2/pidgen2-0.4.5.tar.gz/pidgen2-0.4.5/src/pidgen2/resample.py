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
import math

from . import init

#from jax import numpy as np
#import numpy as onp
import numpy as np
import uproot
from scipy.ndimage import gaussian_filter, convolve

from .tuples import write_array, write_friend_array, read_array
from .resampling import calib_transform, data_transform, get_or_create_template, resample_data
from .resampling import get_samples, get_variables

# Function to create N-dimensional parabolic kernel
def create_parabolic_kernel(bandwidth):
    """
    Create an N-dimensional parabolic kernel.

    Parameters:
    bandwidth: Scaling factors for each dimension of parabolic kernel (tuple of floats/ints).

    Returns:
    kernel: N-dimensional parabolic kernel.
    """
    # Create a coordinate grid
    ranges = []
    for bw in bandwidth :
      size = int(math.ceil(bw))
      ranges += [np.linspace(-size, size, size)]
    grid = np.meshgrid(*ranges, indexing='ij')

    # Calculate squared Euclidean distance from the center in N-dimensions
    distance_squared = np.zeros_like(grid[0])
    for g,bw in zip(grid, bandwidth):
        distance_squared += g**2/bw**2

    # Apply the kernel formula: max(1 - (r/a)^2, 0)
    kernel = np.maximum(1 - distance_squared, 0)
    return kernel

def resample(
    resampling_seed = 1000, 
    input = None, 
    output = None, 
    outtree = "tree", 
    sample = None, 
    dataset = None, 
    variable = None, 
    branches = "pt:eta:ntr", 
    pidgen = "pidgen", 
    stat = "pidstat", 
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
    cachedir = None, 
    eta_from_p = False, 
    nan = -1000., 
    scale = None, 
    parabolic = False, 
    filter_func = None
  ) : 

  input_branches = branches.split(":") if isinstance(branches, str) else branches

  config = get_samples()[sample][dataset]

  pp = pprint.PrettyPrinter(indent = 4)

  if "aliases" in config and variable in config["aliases"] : 
    aliased_variable = config["aliases"][variable]
    if verbose >= 0 :
      print(f"Using alias '{aliased_variable}' for variable name '{variable}' in dataset '{dataset}', sample '{sample}'")
    variable = aliased_variable

  vardef = get_variables()[variable]

  if verbose >= 1 : 
    print(f"Calibration sample config: {pp.pformat(config)}")
    print(f"Variable definition: {pp.pformat(vardef)}")

  if verbose >= 0 :
    print(f"Checking if template exists in the storage")

  #print(cachedir is None)

  # Loop over kernels
  kernel_list = kernels
  if not isinstance(kernels, (list, tuple)) : 
    kernel_list = [ kernels ]

  first_kernel = kernel_list[0]
  if first_kernel and not isinstance(first_kernel, str) : first_kernel = first_kernel[0]

  # Create PID resampling template based on calibration sample
  counts, counts2, edges, normaliser = get_or_create_template(sample, dataset, variable, 
                             vardef, config, kernels = first_kernel, 
                             use_calib_cache = usecache, max_files = maxfiles, 
                             interactive_plots = interactive, 
                             control_plots = plot, verbose = verbose, 
                             local_prefix = local_storage, 
                             global_prefix = global_storage, 
                             cachedir = cachedir)

  from numpy.lib.recfunctions import structured_to_unstructured as s2u
  input_df = uproot.concatenate(input, input_branches, library = "ak")
  input_data = s2u(input_df[input_branches]).to_numpy()

  start_event = start
  stop_event = stop

  if (stop_event is not None) and stop_event > len(input_data) : stop_event = len(input_data)
  else : input_data = input_data[start_event:stop_event]
  if verbose >= 1 : print (f"Shape of the array for resampling: {input_data.shape}")

  if eta_from_p : 
    # Replace momentum by eta calculated from p and pT
    input_data[:,1] = -np.log(np.tan(np.arcsin(input_data[:,0]/input_data[:,1])/2.))

  if not friend :
    if verbose >= 1 :
      all_branches = list(uproot.open(input).keys())
      print (f"List of all input tree branches: {pp.pformat(all_branches)}")

  # Evaluate scaling list if it is a string
  if isinstance(scale, str) : 
    scale_list = eval(scale)
  else : 
    scale_list = scale

  output_arrays = []
  output_branches = []

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
      else : 
        sampled_counts = counts

      if parabolic : 
        if verbose >= 0 :
          print(f"Applying convolution with parabolic kernel {template_sigma}")
        # Multiply sigma in each dim by 5 to roughly match Gaussian smoothing bandwidth
        parabolic_kernel = create_parabolic_kernel([5*s for s in template_sigma])
        parabolic_kernel /= np.sum(parabolic_kernel)
        smooth_counts = convolve(sampled_counts, parabolic_kernel)
      else : 

        if filter_func is None : 
          if verbose >= 0 :
            print(f"Applying Gaussian smearing with kernel {template_sigma}")
          smooth_counts = gaussian_filter(sampled_counts, template_sigma)
        else : 
          if verbose >= 0 :
            print(f"Applying custom filter with kernel {template_sigma}")
          smooth_counts = filter_func(sampled_counts, template_sigma)

      template = smooth_counts, edges, normaliser

      if verbose >= 0 :
        print(f"Smeared template ready, starting resampling")

      np.random.seed(resampling_seed)

      data = data_transform(input_data, config, scale = scale_list )
      pid_arr, calib_stat = resample_data(data, config, vardef, template, verbose = verbose)

      if not (nan is None) : 
        pid_arr = np.nan_to_num(pid_arr, nan = nan)

      output_arrays += [ pid_arr, calib_stat ]
      if (template_seed is None) or (template_seed == 0) : 
        output_branches += [ f"{pidgen}_{kernel_name}", f"{stat}_{kernel_name}" ]
      else : 
        output_branches += [ f"{pidgen}_{kernel_name}_{template_seed}", f"{stat}_{kernel_name}_{template_seed}" ]

      if verbose >= 1 : 
        print(f"Input data array: {input_data[:100]}")
        print(f"Data array after variable transformation: {data[:100]}")
        print(f"Resampled PID array: {pid_arr[:100]}")
        print(f"Resampling statistics array: {calib_stat[:100]}")

  # End of loop over kernels

  if not friend : 
    write_array(output, np.asarray(np.concatenate(output_arrays, axis = 1)),
            branches = output_branches, input = input, tree = outtree, step_size = step_size, 
            library = library, verbose = verbose)
  else : 
    write_friend_array(output, np.asarray(np.concatenate(output_arrays, axis = 1)), 
            branches = output_branches, tree = outtree )

def main() : 

  parser = argparse.ArgumentParser(description = "PIDGen2 resampling script", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--resampling_seed', type=int, default = 1, 
                      help="Initial random seed for resampling")
  parser.add_argument('--input', type=str, default = None, 
                      help="Input ROOT path (file:tree), wildcards allowed")
  parser.add_argument('--output', type=str, default = None, 
                      help="Output ROOT file")
  parser.add_argument('--outtree', type=str, default = "tree", 
                      help="Output TTree")
  parser.add_argument('--sample', type=str, default = None, 
                      help="Calibration sample name")
  parser.add_argument('--dataset', type=str, default = None, 
                      help="Calibration dataset in the form Polarity_Year, e.g. MagUp_2018")
  parser.add_argument('--variable', type=str, default = None, 
                      help="PID variable to resample")
  parser.add_argument('--branches', type=str, default = "pt:eta:ntr", 
                      help="Input branches for Pt,Eta,Ntracks variables in the form Pt:Eta:Ntrack")
  parser.add_argument('--pidgen', type=str, default = "pidgen", 
                      help="Resampled PID branch")
  parser.add_argument('--stat', type=str, default = "pidstat", 
                      help="PID calibration statistics branch")
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
  parser.add_argument('--cachedir', type=str, default = None, 
                      help="Local calibration sample cache directory")
  parser.add_argument('--eta_from_p', default = False, action = "store_const", const = True, 
                      help='Calculate eta from p and pT branches')
  parser.add_argument('--nan', type=float, default = -1000., 
                      help="Numerical value to replace NaN in resampled PID (when calibration data is missing)")
  parser.add_argument('--scale', type=str, default = None, 
                      help="List of scale factors for input data e.g. --scale='1,1,1.15' for 15%% upscaling of multiplicity")
  parser.add_argument('--parabolic', default = False, action = "store_const", const = True, 
                      help='Apply convolution with parabolic kernel for compatibility with old PIDGen instead of Gaussian smearing')

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  resample(**vars(args))

if __name__ == "__main__" : 
  main()
