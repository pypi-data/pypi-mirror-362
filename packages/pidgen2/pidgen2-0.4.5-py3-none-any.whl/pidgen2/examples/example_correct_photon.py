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

import os
import sys

## START OF CONFIG

# Read comments and check vars at least until the end of config section

# List of input ROOT files with MC ntuples. Format:
#   (inputfile, outputfile, dataset)
# outputfile should be without the ".root" extension
# (it will be appended by the variable names when writing friend trees)
files = [
  ("root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/photon/mc_run0_mode0.root", "run1_photon_pidcorr", "2011-2012"),
]

# Name of the input tree
# Could also include ROOT directory, e.g. "Dir/Tree"
input_tree = "DecayTree"

# Postfixes of the Pt, Eta and Ntracks variables (ntuple variable name the particle name part)
# e.g. if the ntuple contains "pi_PT" for the particle "pi", it should be just "PT"
ptvar  = "PT"
etavar = None
pvar   = "P"

simversion = "Sim09"

friend = True       # If True, write friend trees with resampled PID instead of copying the whole tree

scale = (1, 1)      # List of scale factors for each dimension of input data

# List of (kernel, seeds) combinations for raw template smearing
kernels = [
  ('default',    [0, 1, 2, 3]),   # Default kernel width, no template sampling 
                                  # and three "bootstrapped" templates with seeds 1..3
  ('syst1',      [0]),            # Wider "syst1" kernel, no template sampling 
]

# Configuration dictionary for resampling, in the form {particle_name}:{pidvars}
# For each {particle_name}, {pidvars} is a dictionary in the form {corrected_variable}:({original_variable}, {sample}, {PID_var}, {kernels}),
#   where
#     {corrected_variable} is the name of the corrected ntuple PID variable without the particle name part
#                       (e.g. for "pi_PIDK" branch of particle "pi" it should be just "PIDK"); 
#     {original_variable} is the name of the original ntuple PID variable without the particle name part
#     {sample} is the name of the calibration sample
#     {PID_var} is the string describing the PID variable template.
#     {kernels} is the list of kernels for template smearing (see example above)
# 
# Run pidgen2.list_variables to get the full list of PID variables
# Run pidgen2.list_samples to get the full list of calibration samples

config = {
  'gamma' : {
              "CL"       : ("CL", "gamma_B2KstarGammaType0", "PhotonCL", kernels),
              "IsPhoton" : ("PP_IsPhoton", "gamma_B2KstarGammaType0", "IsPhoton", kernels),
            },
}

## END OF CONFIG

output_tree = input_tree.split("/")[-1]
treename = input_tree

from pidgen2.correct import correct

for input_file, output_file, dataset in files :

  input_location = f"{input_file}:{input_tree}"

  for track, subst in config.items() :
    for var, (pidvar, sample, calibvar, kernel_list) in subst.items() :

      # Create the list of input branches, depending on whether Eta or P variable is available
      if pvar is None : 
        branches = f"{track}_{pidvar}:{track}_{ptvar}:{track}_{etavar}"
        eta_from_p = False
      else : 
        branches = f"{track}_{pidvar}:{track}_{ptvar}:{track}_{pvar}"
        eta_from_p = True

      if friend : 
         output_root_file = f"{output_file}_{track}_{var}.root"
      else : 
         output_root_file = f"{output_file}.root"

      # Run resampling of a single variable in a single file
      correct(
         input = input_location,    # Input tuple
         simversion = simversion,   # Simulation version of the input MC file
         sample = sample,           # Calibration sample (e.g. "pi_Dstar2Dpi")
         dataset = dataset,         # Dataset (e.g. "MagUp_2016")
         variable = calibvar,       # Calibration variable (e.g. "MC15TuneV1_ProbNNK")
         branches = branches,       # List of resampling branches (typically, corresponding to Pt, Eta and Ntracks, e.g. "pt:eta:ntr")
         output = output_root_file, # Output ROOT file name
         outtree = output_tree,     # Output tree name
         plot = True,               # If template needs to be created from scratch, produce control plots
         pidcorr = f"{track}_{var}_pidcorr",  # Name of the corrected PID branch
         stat = f"{track}_{var}_pidstat",     # Name of output branch with calibration statistics for each resampled event
         mcstat = f"{track}_{var}_pidmcstat", # Name of output branch with MC statistics for each resampled event
         kernels = kernel_list,     # List of kernels and template seeds
         verbose = False,           # Print debugging information
         eta_from_p = eta_from_p,   # If eta needs to be calculated from p and pt
         friend = friend,           # If True, write output to friend trees
         library = "ak",            # Library to handle ROOT files with uproot if friend=False, can be 
                                    # "ak" (Awkward array), "np" (numpy) or "pd" (Pandas)
         step_size = 50000,         # Chunk size when writing files with uproot if friend=False
         nan = -1000.,              # Numerical value to substitute NaN, for regions w/o calibration data 
         scale = scale,             # Scale factors for input data 
         local_storage = "./templates/",  # Directory for local template storage, used when the template is not available in 
                                          # the global storage on EOS. 
         local_mc_storage = "./mc_templates/",  # Directory for local template storage, used when the template is not available in 
                                          # the global storage on EOS. 
      )

      if not friend : 
        # All subsequent calls use output file as input
        input_location = f"{output_root_file}:{output_tree}"
