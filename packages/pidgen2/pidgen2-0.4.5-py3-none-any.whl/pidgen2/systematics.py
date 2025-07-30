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

#Script which takes input a tuple with piddata and resampled pid (pidgen) and plots efficiency as function of cut on pid. 
#Compares data with pidgen.

from jax import numpy as np
import numpy as onp
import matplotlib
import matplotlib.pyplot as plt
import uproot
#import uproot4

import sys
sys.path.append(".")

from .plotting import plot, plot_distr1d_comparison, set_lhcb_style, plot_hist2d
from .tuples import read_array_filtered, write_array, read_array
from .resampling import get_samples, get_variables
from . import density_estimation as de

import argparse

def main() : 

  parser = argparse.ArgumentParser(description = "PIDGen systematics estimation", 
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
  parser.add_argument('--transform', default = False, action="store_const",const=True, 
                      help="Transformed or Untransformed PID variable")

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  def get_effi(pid,sweights,cut):
      import pandas as pd
      d = {"pid":pid,"sw":sweights}
      df = pd.DataFrame(data=d)
      norm = sum(df["sw"])
      df = df.query("pid >"+str(cut))
      effi = sum(df["sw"])/norm
      df=df.reset_index(drop=True)
      return effi,df["pid"],df["sw"],cut

  def plot_diff(x,y,z,ylabel1,ylabel2,xlabel,title,name):
      fig = plt.figure()
      fig, (ax1,ax2) = plt.subplots(1,2,figsize=(15,5))
      fig.suptitle(title)
      ax1.scatter(x,y)
      ax1.set_ylabel(ylabel1)
      ax1.set_xlabel(xlabel)
      ax1.xaxis.set_tick_params(labelsize=5)
      ax2.scatter(x,z)
      ax2.set_ylabel(ylabel2)
      ax2.set_xlabel(xlabel)
      ax2.xaxis.set_tick_params(labelsize=5)
      fig.savefig(name+'.pdf')

  input_tuple = args.input
  input_tree = args.intree

  output_tuple = args.output

  sample_name = args.sample
  dataset_name = args.dataset
  variable_name = args.variable

  config = get_samples()[sample_name][dataset_name]
  variable = get_variables()[variable_name]

  template_sigma = [variable["template_sigma"]] + config["template_sigma"]

  f = uproot.open(input_tuple)
  t = f[input_tree]
  branches = t.keys()

  input_branches = args.branches.split(":") + [args.pidgen,args.piddata, args.weight]
  print("Input branches",input_branches)
  input_data = read_array_filtered(t, input_branches, selection = "pidstat>10", sel_branches = ["pidstat"])
  print (f"input_data shape: {input_data.shape}")

  sw = input_data[:,-1]
  pidgen_tr = input_data[:,-3]  
  piddata_tr = input_data[:,-2]

  #print("pid resampled",input_data[:,-3])
  #print("pid orig",input_data[:,-2])

  set_lhcb_style(size = 12)
  diff_effi=[]
  rel_diff_effi = []
  cuts = onp.linspace(0,0.95,20)
  cuts = onp.append(cuts,[0.96,0.97,0.98])
  for cut in cuts:
      effi_data,_,_,_ = get_effi(piddata_tr,sw,cut) 
      effi_pidgen,_,_,_ = get_effi(pidgen_tr,sw,cut)
      diff_effi += [effi_data - effi_pidgen]
      rel_diff_effi += [(effi_data - effi_pidgen)/effi_data]
  plot_diff(cuts,diff_effi,rel_diff_effi,"(PIDdata-PIDgen) eff","(PIDdata-PIDgen)/PIDdata eff","pidcut","Original data vs resampled ","Diff_eff")

if __name__ == "__main__" : 
  main()
