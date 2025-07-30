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

from ..datasets import legacy_run2_b2jpsieek_stripping_datasets as ds_run2
from ..run3_datasets import get_pidcalib_samples, get_sample_config

from itertools import product

common_params = {
    "calib_cache_branches" : ["pt", "eta", "ntr", "sw"],          # Names of variable branches in ROOT tree of the cache file 
    "data_ranges" : [ (2.4, 4.4), (1.9, 5.0), (0.7, 3.1) ],       # Ranges of each variable after transformation
    "labels" : [r"PID", r"$p_T$", r"$\eta$", r"$N_{\rm tr}$"],    # Labels for plots
    "names" : ["pid", "pt", "eta", "ntr"],                        # Short names of each variable for plot file names
    "max_weights" : None, 
    "smear" : [ None, None, (-0.5, 0.5) ], 
    "transform" : [                                               # Transformation functions for each variable
      "np.log10(x)",   # pT transformation
      "x",             # eta
      "np.log10(x)",   # number of tracks
    ], 
    "normalise_bins" : [100, 100, 100],                           # Number of bins for normalisation of each variable
    "normalise_methods" : ["scale", "scale", "flatten"],          # Normalisation method for each variable ("scale", "normalise", "flatten")
    "normalise_ranges" : 2*[ (0., 1.) ] + [ (0., 1.) ],           # Ranges of each variable after normalisation
    "template_bins" : [70, 70, 20],                               # Number of bins for each variable in the template 
    "template_sigma" : { 
      "default" : [3., 6., 6.],                                   # Smearing parameter for the template for each variable. 
      "syst1"   : [4.5, 9., 9.], 
    }
}

common_params_run3 = {
    "calib_cache_branches" : ["pt", "eta", "ntr", "sw"],          # Names of variable branches in ROOT tree of the cache file 
    "data_ranges" : [ (2.4, 4.4), (1.9, 5.0), (0.7, 3.1) ],       # Ranges of each variable after transformation
    "labels" : [r"PID", r"$p_T$", r"$\eta$", r"$N_{\rm tr}$"],    # Labels for plots
    "names" : ["pid", "pt", "eta", "ntr"],                        # Short names of each variable for plot file names
    "max_weights" : None, 
    "smear" : [ None, None, (-0.5, 0.5) ], 
    "transform" : [                                               # Transformation functions for each variable
      "np.log10(x)",   # pT transformation
      "x",             # eta
      "np.log10(x)",   # number of tracks
    ], 
    "normalise_bins" : [100, 100, 100],                           # Number of bins for normalisation of each variable
    "normalise_methods" : ["scale", "scale", "flatten"],          # Normalisation method for each variable ("scale", "normalise", "flatten")
    "normalise_ranges" : 2*[ (0., 1.) ] + [ (0., 1.) ],           # Ranges of each variable after normalisation
    "template_bins" : [70, 70, 20],                               # Number of bins for each variable in the template 
    "template_sigma" : { 
      "default" : [1., 2., 2.],                                   # Smearing parameter for the template for each variable. 
      "syst1"   : [1.5, 3., 3.], 
    }
}

sample_run2 = {
  f"{pol}_{year}" : { 
    "sample" : ds_run2[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_Brunel_PT", 
      "probe_Brunel_ETA", 
      "nTracks" if year == "2016" else "nTracks_Brunel", 
      "probe_sWeight" 
    ], 
    "trees" : ['DecayTree'], 
    "variables" : [
                   "CombDLLK", "CombDLLmu", "CombDLLe", "CombDLLp", 
                   "MC15TuneV1_ProbNNpi", "MC15TuneV1_ProbNNK", "MC15TuneV1_ProbNNp", 
                   "MC15TuneV1_ProbNNe", "MC15TuneV1_ProbNNmu", 
                  ], 
    "cut" : "probe_Brunel_HasBremAdded==1", 
    **common_params, 
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}

sample = {**sample_run2}
