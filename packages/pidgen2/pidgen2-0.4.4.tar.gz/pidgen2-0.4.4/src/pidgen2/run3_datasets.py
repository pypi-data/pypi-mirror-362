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

import json
import os
import sys

def get_pidcalib_samples() : 
  """
    Load JSON with PIDCalib samples configuration and return corresponding dictionary
  """
  json_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/samples.json"))
  with open(json_file) as f : 
    d = json.load(f)
  return d
  
def list_samples(samples_dict) : 
  return samples_dict.keys()

import re
def wrap_comparisons(expression):
    # Regular expression to match comparison expressions
    comparison_pattern = re.compile(r'(\w+\s*(?:==|!=|<=|>=|<|>)\s*\w+)')

    # Replace each match with itself wrapped in parentheses
    return comparison_pattern.sub(r'(\1)', expression)
  
def get_sample_config(sample, particle, cut = None) : 
  sw_dir = sample["sweight_dir"]
  tuple_names = sample["tuple_names"][particle]
  probe_prefix = sample["probe_prefix"]
  sample_cuts = None
  if "cuts" in sample : sample_cuts = sample["cuts"]
  if cut : 
    if sample_cuts == None : sample_cuts = [ cut ]
    else : sample_cuts += [ cut ]

  files = []
  for f in sample["files"] : 
    basename = f.split("/")[-1].split(".")[0]
    swf = sw_dir + "/" + basename + ".pid_turboraw_tuple_sweights.root"
    files += [ (f, swf) ]

  config = {
    "sample" : files, 
    "prefix" : probe_prefix, 
    "expressions" : [ 
      probe_prefix + "_PT", 
      probe_prefix + "_ETA", 
      "nLongTracks", 
      "sweight" 
    ], 
    "branches" : [ 
      probe_prefix + "_PT", 
      probe_prefix + "_ETA", 
      "nLongTracks", 
      "sweight" 
    ], 
    "trees" : [ n + "/DecayTree" for n in tuple_names ], 
    "variables" : ["PID_K", "PID_MU", "PID_E", "PID_P", 
                   "PROBNN_K", "PROBNN_MU", "PROBNN_E", "PROBNN_P", "PROBNN_PI" 
                  ]
  }
  if sample_cuts : 
    config["cut"] = wrap_comparisons(" & ".join( [ f"({i})" for i in sample_cuts ] ))

  return config
