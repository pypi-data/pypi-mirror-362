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
import pprint

#from jax import numpy as np
#import numpy as onp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import uproot
import functools
from scipy.ndimage import gaussian_filter

import argparse

from .plotting import plot_distr1d_comparison, set_lhcb_style, plot_hist2d, plot
from .tuples import read_array_filtered, write_array, read_array
from .resampling import get_samples, get_variables

def validate(
    input = None, 
    intree = None, 
    sample = None, 
    dataset = None, 
    variable = None, 
    weight = None, 
    branches = None, 
    pidgen = "pidgen", 
    piddata = "pid", 
    output = None, 
    verbose = False, 
    interactive = False, 
    selection = None
  ) : 

  input_branches = branches.split(":") + [pidgen, piddata, weight]

  pp = pprint.PrettyPrinter(indent = 4)

  config = get_samples()[sample][dataset]
  vardef = get_variables()[variable]

  if (verbose) : 
    print(f"Calibration sample config: {pp.pformat(config)}")
    print(f"Variable definition: {pp.pformat(vardef)}")

  f = uproot.open(input)
  t = f[intree]
  branches = t.keys()
  if (verbose) : print (f"List of all input tree branches: {pp.pformat(branches)}")
  #input_data = read_array_filtered(t, input_branches, selection = selection, sel_branches = ["pidstat"])
  input_data = t.arrays(input_branches, selection, library = "pd")[input_branches].to_numpy()
  if (verbose) : print (f"Input data array shape: {input_data.shape}")

#  transform_forward = lambda x: 1.-(1.-x)**0.2
  transform_forward = eval("lambda x : (" + vardef["transform_forward"] + ")")

  pidgen_tr = transform_forward(input_data[:,-3])
  piddata_tr = transform_forward(input_data[:,-2])
  sw = input_data[:,-1]

  if (verbose) : print(f"Array of sWeights: {sw}")

  label = variable

  set_lhcb_style(size = 12, usetex = False)

  with plot("", output, (5., 4.)) as (fig, ax) : 
    plot_distr1d_comparison(piddata_tr, pidgen_tr, bins = 100, range = vardef["data_range"], ax = ax, 
       label = "Transformed PID", 
       weights = sw, data_weights = sw, 
       title = "Transformed PID", log = False, pull = True, 
       legend = ["Original distribution", "Resampled distribution"], 
       data_alpha = 0.5)

  if (interactive) : plt.show()


def main() : 

  parser = argparse.ArgumentParser(description = "PIDGen2 validation script", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--input', type=str, default = None, 
                      help="Input ROOT file")
  parser.add_argument('--intree', type=str, default = None, 
                      help="Input TTree")
  parser.add_argument('--sample', type=str, default = None, 
                      help="Calibration sample name")
  parser.add_argument('--dataset', type=str, default = None, 
                      help="Calibration dataset in the form Polarity_Year, e.g. MagUp_2018")
  parser.add_argument('--variable', type=str, default = None, 
                      help="PID variable to resample")
  parser.add_argument('--weight', type=str, default = None, 
                      help="Weigth branch name")
  parser.add_argument('--branches', type=str, default = "pt:eta:ntr", 
                      help="Input branches for Pt,Eta,Ntracks variables in the form Pt:Eta:Ntrack")
  parser.add_argument('--pidgen', type=str, default = "pidgen", 
                      help="Resampled PID branch")
  parser.add_argument('--piddata', type=str, default = "pid", 
                      help="Original PID branch")
  parser.add_argument('--output', type=str, default = None, 
                      help="Output prefix")
  parser.add_argument('--selection', type=str, default = None, 
                      help="Selection string")
  parser.add_argument('--verbose', default = False, action = "store_const", const = True, 
                      help='Enable debug messages')
  parser.add_argument('--interactive', default = False, action = "store_const", const = True, 
                      help='Open interactive plot window (if False, only store the pdf file). ')

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  validate(**vars(args))

if __name__ == "__main__" : 
  main()
