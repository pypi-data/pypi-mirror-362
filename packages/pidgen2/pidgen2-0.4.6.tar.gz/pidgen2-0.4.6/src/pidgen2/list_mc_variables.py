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

import pprint
import sys

from .resampling import get_variables
from .resampling import get_mc_samples

def main() : 

  variables = get_variables().keys()

  if len(sys.argv)==1 : 
  
    print("List available PIDGen2 calibration variables in MC samples (only needed for pidgen2.correction). Usage: ")
    print("  pidgen2.list_mc_variables [dataset] [sample]")
    print("e.g.")
    print("  pidgen2.list_mc_variables K_Dstar2Dpi MagUp_2018")
    print("The full list of available variables is as follows: ")

    for v in sorted(variables) : 
      print(f"  {v}")

  elif len(sys.argv)==2 : 

    ds = sys.argv[1]
    samples = get_mc_samples()
    if ds not in samples : 
      print(f"Dataset '{ds}' is not available")

    else : 
      print(f"The list of available MC samples for dataset {ds} is: ")
      for s in samples[ds].keys() : 
        print(f"  {s}")      
      
  else : 
    
    ds = sys.argv[1]
    s = sys.argv[2]
    samples = get_mc_samples()
    if ds not in samples : 
      print(f"Dataset '{ds}' is not available")
    else : 
      if s not in samples[ds] : 
        print(f"Sample '{s}' is not available for dataset '{ds}'")
      else : 
        for v in samples[ds][s]["variables"] : 
          if v not in variables : 
            print(f"  variable '{v}' is not in the global list of variables, please check...")
          else : 
            print(f"  {v}")

if __name__ == "__main__" : 
  main()
