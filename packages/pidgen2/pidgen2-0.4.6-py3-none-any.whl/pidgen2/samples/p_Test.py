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

from ..mc_datasets import lb2jpsipk_run2sim09_datsets as mc_run2sim09

common_params = {
    "smear" : [ None, None, (-0.5, 0.5) ], 
    "transform" : [ 
      "np.log10(x)",   # pT transformation
      "x",             # eta
      "np.log10(x)",   # number of tracks
    ], 
    "calib_cache_branches" : ["pt", "eta", "ntr"], 
    "data_ranges" : [ (2.4, 4.4), (1.9, 5.0), (0.7, 3.1) ], 
    "labels" : [r"PID", r"$p_T$", r"$\eta$", r"$N_{\rm tr}$"],    # Labels for plots
    "names" : ["pid", "pt", "eta", "ntr"],                        # Short names of each variable for plot file names
    "max_weights" : None, 
    "normalise_bins" : [100, 100, 100], 
    "normalise_methods" : ["scale", "scale", "flatten"], 
    "normalise_ranges" : 3*[ (0., 1.) ], 
    "template_bins" : [70, 70, 20], 
    "template_sigma" : {
      "default" : [2., 4., 4.], 
      "syst1"   : [3., 6., 6.], 
    }
}

mc_sample_run2 = {
  f"Sim09_{pol}_{year}" : {
    "sample" : mc_run2sim09[f"{pol}_{year}"], 
    "branches" : [
      "p_PT", 
      "p_ETA", 
      "nTracks",
    ], 
    "trees" : ["lc/nt"], 
    "variables" : ["Test_ProbNNp"], 
    **common_params, 
  }
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}

sample_run2 = {
  f"{pol}_{year}" : {
    "sample" : mc_run2sim09[f"{pol}_{year}"], 
    "branches" : [
      "p_PT", 
      "p_ETA", 
      "nTracks",
    ], 
    "trees" : ["lc/nt"], 
    "variables" : ["Test_ProbNNp"], 
    **common_params, 
  }
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}

sample = {**sample_run2}
mc_sample = {**mc_sample_run2 }
