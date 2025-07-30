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

import os, sys

def main() : 

  if len(sys.argv)<2 : 
    print("This is a script to create an example Python file for PIDGen2 photon ID correction.")
    print("Usage: pidgen2.create_photon_correction_example examplefilename.py")
  else : 
    outputname = sys.argv[1]
    inputname = os.path.dirname(os.path.abspath(__file__)) + "/examples/example_correct_photon.py"
    os.system(f"cp {inputname} {outputname}")

if __name__ == "__main__" : 
  main()
