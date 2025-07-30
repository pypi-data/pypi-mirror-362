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

variable = {
    "expression" : "{prefix}_PID_P", 
    "mc_expression" : "{prefix}_PID_P", 
    "data_range" : (-150., 150.), 
    "transform_forward" : "x", 
    "transform_backward" : "x", 
    "normalise_bins" : 1000, 
    "normalise_method" : "gauss", 
    "normalise_range" : (-2.5, 2.5), 
    "template_bins" : 70, 
    "template_sigma" : {
      "default" : 1., 
      "syst1"  : 1.5, 
    }, 
    "resample_bins" : 200, 
}
