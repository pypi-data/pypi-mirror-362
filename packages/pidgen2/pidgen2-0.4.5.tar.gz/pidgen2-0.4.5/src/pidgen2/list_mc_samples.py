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

from .resampling import get_mc_samples

def main() : 

  samples = get_mc_samples()

  if len(sys.argv)<2 : 
    print("List available PIDGen2 MC samples (needed only for pidgen2.correction). Usage: ")
    print("  pidgen2.list_mc_samples [dataset]")
    print("Available datasets are: ")
    for ds in sorted(samples.keys()) : 
      print(f"  {ds}")

  else : 
    ds = sys.argv[1]
    if ds not in samples.keys() : 
      print(f"Dataset '{ds}' is not available.")
    else : 
      for s in samples[ds].keys() : 
        print(f"  {s}")

if __name__ == "__main__" : 
  main()
