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

from ..datasets import legacy_run2_pidcalib_datasets as ds_run2
from ..datasets import converted_run1_pidcalib_datasets_lam0_p as ds_run1
from ..mc_datasets import lb2jpsipk_run2sim09_datsets as mc_run2sim09
from ..mc_datasets import lcmu_run1sim09_datasets as mc_run1sim09
from ..run3_datasets import get_pidcalib_samples, get_sample_config

from itertools import product
from copy import copy

probnn_responses = ["pi", "K", "p", "e", "mu", "piNotK", "piNotKp", "KNotpi", "KNotpip", "pNotK", "pNotpiK"]

def brunel_aliases(year) : 
    """
      Define aliases for Brunel variables in 2017, 2018 samples
      to point to Online versions. 
    """
    if year in ["2017", "2018"] : 
        return { "Brunel_MC15TuneV1_ProbNN" + var : "MC15TuneV1_ProbNN" + var for var in probnn_responses }
    else : return {}

probnn_responses_mc = ["pi", "K", "p"]
brunel_aliases_mc = { "Brunel_MC15TuneV1_ProbNN" + var : "MC15TuneV1_ProbNN" + var for var in probnn_responses_mc }

def trees(year) : 
  #return [ ("Lam0" + ("LL" if year in ["2017", "2018"] else "") + \
  #            f"_{i}{j}Tuple/DecayTuple") for i, j in product(["", "HPT_", "VHPT_"], ["P", "Pbar"]) ]
  return [ (f"Lam0LL_{i}{j}Tuple/DecayTree") for i, j in product(["", "HPT_", "VHPT_"], ["P", "Pbar"]) ]

common_params = {
    "smear" : [ None, None, (-0.5, 0.5) ], 
    "transform" : [ 
      "np.log10(x)",   # pT transformation
      "x",             # eta
      "np.log10(x)",   # number of tracks
    ], 
    "calib_cache_branches" : ["pt", "eta", "ntr", "sw"], 
    "data_ranges" : [ (2.4, 4.4), (1.9, 5.0), (0.7, 3.1) ], 
    "labels" : [r"PID", r"$p_T$", r"$\eta$", r"$N_{\rm tr}$"],    # Labels for plots
    "names" : ["pid", "pt", "eta", "ntr"],                        # Short names of each variable for plot file names
    "max_weights" : (40., 1., 1.), 
    "normalise_bins" : [100, 100, 100], 
    "normalise_methods" : ["flatten", "flatten", "flatten"], 
    "normalise_ranges" : 3*[ (0., 1.) ], 
    "template_bins" : [70, 70, 20], 
    "template_sigma" : {
      "default" : [2., 4., 4.], 
      "syst1"   : [3., 6., 6.], 
    }
}

sample_run2 = {
  f"{pol}_{year}" : { 
    "sample" : ds_run2[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_Brunel_PT", 
      "probe_Brunel_ETA", 
      "nTracks_Brunel", 
      "probe_sWeight" 
    ], 
    "trees" : trees(year), 
    "variables" : ["CombDLLK", "CombDLLmu", "CombDLLe", "CombDLLp"] + 
                  [ f"{b}MC15TuneV1_ProbNN{i}" for b, i in product(["", "Brunel_"], probnn_responses) ], 
    "aliases" : brunel_aliases(year), 
    **common_params
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}

sample_run1 = {
  f"{pol}_{year}" : { 
    "sample" : ds_run1[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_PT", 
      "probe_ETA", 
      "nTracks", 
      "probe_sWeight" 
    ], 
    "trees" : ["DecayTree"], 
    "variables" : [
                   "CombDLLK", "CombDLLmu", "CombDLLe", "CombDLLp", 
                   "MC12TuneV2_ProbNNpi", "MC12TuneV2_ProbNNK", "MC12TuneV2_ProbNNp", 
                   "MC12TuneV3_ProbNNpi", "MC12TuneV3_ProbNNK", "MC12TuneV3_ProbNNp", 
                   "MC12TuneV3_ProbNNe", "MC12TuneV3_ProbNNmu", 
                   "MC12TuneV3_ProbNNpiNotK", "MC12TuneV3_ProbNNpiNotKp", 
                   "MC12TuneV3_ProbNNKNotpi", "MC12TuneV3_ProbNNKNotpip", 
                   "MC12TuneV3_ProbNNpNotK", "MC12TuneV3_ProbNNpNotpiK", 
                  ], 
    **common_params
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2011", "2012"]
}

run3_sample_dict = get_pidcalib_samples()
run3_p_datasets = [
  '2024_WithUT_block1_v0-MagUp-P', 
  '2024_WithUT_block1_v1-MagUp-P', 
  '2024_WithUT_block2-MagUp-P', 
  '2024_WithUT_block3-MagUp-P', 
  '2024_WithUT_block5-MagUp-P', 
  '2024_WithUT_block6-MagDown-P', 
  '2024_WithUT_block7-MagDown-P', 
  '2024_WithUT_block8-MagUp-P', 
  '2024-MagUp-P', 
  '2024-MagDown-P'
]

sample_run3 = {
  s : {
    **common_params, 
    **get_sample_config(run3_sample_dict[s], "P"), 
  }
  for s in run3_p_datasets
}

mc_params = copy(common_params)
mc_params['max_weights'] = None

mc_sample_run1 = {
  f"Sim09_{pol}_{year}" : {
    "sample" : mc_run1sim09[f"{pol}_{year}"],
    "prefix" : "p", 
    "branches" : [
      "p_PT", 
      "p_ETA", 
      "nTracks", 
    ], 
    "trees" : ["tree"], 
    "variables" : [ f"MC12TuneV2_ProbNN{i}" for i in probnn_responses_mc ] + 
                  [ f"MC12TuneV3_ProbNN{i}" for i in probnn_responses_mc ] + 
                  ["CombDLLp", "CombDLLK"], 
    **mc_params, 
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2011", "2012"]
}

mc_sample_run2 = {
  f"Sim09_{pol}_{year}" : {
    "sample" : mc_run2sim09[f"{pol}_{year}"], 
    "prefix" : "p", 
    "branches" : [
      "p_PT", 
      "p_ETA", 
      "nTracks",
    ], 
    "trees" : ["lc/nt"], 
    "variables" : [ f"{b}MC15TuneV1_ProbNN{i}" for b, i in product(["", "Brunel_"], probnn_responses_mc) ] + 
                  ["CombDLLp", "CombDLLK"], 
    "aliases" : brunel_aliases_mc, 
    **mc_params, 
  }
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}

sample = {**sample_run1, **sample_run2, **sample_run3 }
mc_sample = {**mc_sample_run1, **mc_sample_run2 }
