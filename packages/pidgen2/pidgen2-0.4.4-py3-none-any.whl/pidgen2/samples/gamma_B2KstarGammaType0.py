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

from ..datasets import photon_run1_datasets_kstargamma_partreco_type0 as ds_run1
from ..datasets import photon_run2_datasets_kstargamma_partreco_type0 as ds_run2

from ..mc_datasets import photon_run1sim09_datasets_kstargamma as mc_ds_run1sim09
from ..mc_datasets import photon_run2sim09_datasets_kstargamma as mc_ds_run2sim09

from itertools import product

eta_from_p = "arctanh(sqrt(gamma_P**2-gamma_PT**2)/gamma_P)"

common_params = {
    "calib_cache_branches" : ["pt", "eta", "sw"],          # Names of variable branches in ROOT tree of the cache file 
    "data_ranges" : [ (3.48, 4.4), (1.5, 4.7) ],           # Ranges of each variable after transformation
    "labels" : [r"CL($\gamma$)", r"$p_T$", r"$\eta$" ],    # Labels for plots
    "names" : ["pid", "pt", "eta"],                        # Short names of each variable for plot file names
    "max_weights" : None, 
    "smear" : [ None, None ], 
    "transform" : [                                               # Transformation functions for each variable
      "np.log10(x)",   # pT transformation
      "x",             # eta
    ], 
    "normalise_bins" : [100, 100],                           # Number of bins for normalisation of each variable
    "normalise_methods" : ["scale", "scale"],                # Normalisation method for each variable ("scale", "normalise", "flatten")
    "normalise_ranges" : 2*[ (0., 1.) ],                     # Ranges of each variable after normalisation
    "template_bins" : [70, 70],                              # Number of bins for each variable in the template 
    "template_sigma" : { 
      "default" : [3., 6.],                                  # Smearing parameter for the template for each variable. 
      "syst1"   : [4.5, 9.], 
    }
}

sample_run1 = {
  year : { 
    "sample" : ds_run1[year], 
    "expressions" : [ 
      "gamma_PT", 
      eta_from_p, 
      "wt_sig"
    ], 
    "branches" : [ 
      "gamma_PT", 
      "gamma_P", 
      "wt_sig"
    ], 
    "trees" : ['DecayTree'], 
    "variables" : ["PhotonCL", "IsPhoton"], 
    **common_params, 
  } 
  for year in ["2011-2012"]
}

mc_sample_run1 = {
  f"Sim09_{year}" : { 
    "sample" : mc_ds_run1sim09[year], 
    "expressions" : [ 
      "gamma_PT", 
      eta_from_p, 
    ], 
    "branches" : [ 
      "gamma_PT", 
      "gamma_P", 
    ], 
    "trees" : ['DecayTree'], 
    "variables" : ["PhotonCL", "IsPhoton"], 
    **common_params, 
  } 
  for year in ["2011-2012"]
}

sample_run2 = {
  year : { 
    "sample" : ds_run2[year], 
    "expressions" : [ 
      "gamma_PT", 
      eta_from_p, 
      "wt_sig"
    ], 
    "branches" : [ 
      "gamma_PT", 
      "gamma_P", 
      "wt_sig"
    ], 
    "trees" : ['DecayTree'], 
    "variables" : ["PhotonCL", "IsPhoton"], 
    **common_params, 
  } 
  for year in ["2016", "2017", "2018"]
}

mc_sample_run2 = {
  f"Sim09_{year}" : { 
    "sample" : mc_ds_run2sim09[year], 
    "expressions" : [ 
      "gamma_PT", 
      eta_from_p, 
    ], 
    "branches" : [ 
      "gamma_PT", 
      "gamma_P", 
    ], 
    "trees" : ['DecayTree'], 
    "variables" : ["PhotonCL", "IsPhoton"], 
    **common_params, 
  } 
  for year in ["2016", "2017", "2018"]
}

sample = {**sample_run1, **sample_run2}
mc_sample = {**mc_sample_run1, **mc_sample_run2}
