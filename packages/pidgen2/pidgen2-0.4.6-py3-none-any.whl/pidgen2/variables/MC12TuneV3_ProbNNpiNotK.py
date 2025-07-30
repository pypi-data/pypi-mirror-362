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
    "expression" : "probe_MC12TuneV3_ProbNNpi*(1.-probe_MC12TuneV3_ProbNNk)", 
    "branches" : ["probe_MC12TuneV3_ProbNNk", "probe_MC12TuneV3_ProbNNpi"], 
    "data_range" : (0., 1.), 
    "transform_forward" : "1.-(1.-x**0.25)**0.5", 
    "transform_backward" : "(1.-(1.-x)**2)**4", 
    "normalise_bins" : 1000, 
    "normalise_method" : "gauss", 
    "normalise_range" : (-2.5, 2.5), 
    "template_bins" : 70, 
    "template_sigma" : {
      "default" : 2., 
      "syst1"  : 3., 
    }, 
    "resample_bins" : 200, 
}
