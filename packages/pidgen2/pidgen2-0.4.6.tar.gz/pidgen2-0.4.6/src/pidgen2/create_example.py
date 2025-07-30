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
import argparse

examples = {
  ('resample', 'run2', False, False) : "example_resample.py", 
  ('resample', 'run3', False, False) : "example_resample_run3.py", 
  ('correct',  'run2', False, False) : "example_correct.py", 
  ('correct',  'run2', True, False)  : "example_correct_photon.py", 
  ('resample', 'run2', False, True)  : "example_numpy_resampler.py", 
  ('correct',  'run2', False, True)  : "example_numpy_corrector.py", 
}

def main() : 

  parser = argparse.ArgumentParser(description = "Create PIDGen2 example script", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument("output", type=str, default = None, help="Output file name")
  parser.add_argument("--method", type=str, default = None, choices = ['resample', 'correct'], 
                      help="PID generation method")
  parser.add_argument("--run", type=str, default = None, choices = ['run2', 'run3'], 
                      help="Run period")
  parser.add_argument("--photon", action="store_true", help="Photon resampling (default is charged tracks)")
  parser.add_argument("--numpy", action="store_true", help="Numpy interface (default is uproot)")

  args = parser.parse_args()

  if not args.method or not args.run or not args.output : 
    parser.print_help()
    raise SystemExit
  else : 
    comb = (args.method, args.run, args.photon, args.numpy)
    path = os.path.dirname(os.path.abspath(__file__)) + "/examples/"
    if comb in examples : 
      os.system(f"cp {path + examples[comb]} {args.output}")
    else : 
      print("Example file for this combination is not available. Available ones are: ")
      for k in examples.keys() : 
        print(f"  --method={k[0]} --run={k[1]}{' --photon' if k[2] else ''}{' --numpy' if k[3] else ''}")

if __name__ == "__main__" : 
  main()
