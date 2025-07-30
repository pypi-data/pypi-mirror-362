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

# Example of numpy API independent of uproot. 
# Allows one to correct the PID response from the pid, pt, eta and Ntracks values 
# stored in the numpy array of shape (N, 4) (where N is the number of candidates)

import numpy as np
from pidgen2.corrector import create_corrector

sample = "K_Dstar2Dpi"
dataset = "MagDown_2016"
calibvar = "MC15TuneV1_ProbNNK"
kernel = ("default", 0)
scale = None

# Create corrector function initialised with the sample, dataset etc. 

corrector = create_corrector(
         sample = sample,           # Calibration sample (e.g. "pi_Dstar2Dpi")
         dataset = dataset,         # Dataset (e.g. "MagUp_2016")
         variable = calibvar,       # Calibration variable (e.g. "MC15TuneV1_ProbNNK")
         simversion = "Sim09", 
         plot = False,              # If template needs to be created from scratch, produce control plots
         kernel = kernel,           # List of kernels and template seeds
         verbose = -1,              # Print debugging information
         nan = -1000.,              # Numerical value to substitute NaN, for regions w/o calibration data 
         scale = scale,             # Scale factors for input data 
         local_storage = "./templates/", # Directory for local template storage, used when the template is not available in 
                                         # the global storage on EOS. 
         local_mc_storage = "./mc_templates/", # Directory for local template storage, used when the template is not available in 
                                               # the global storage on EOS. 
      )

# Create the numpy structure for 4 tracks 
# (the last track is intentionally outside of the kinematic region)
pid = [0.7, 0.8, 0.9, 0.99]
pt = [1000., 2000., 3000., 1.]
eta = [3.5, 4.5, 2.5, 0.]
ntr = [100., 300., 200., 1.]

data = np.array([pid, pt, eta, ntr], dtype = float).T

print("Input data: ")
print(data)

# Run corrector on the numpy array. 
# The output is three 1D arrays of length N, 
#   pid : resampled PID response
#   stat : per-event statistics of the calibration sample
#   mcstat : per-event statistics of the MC sample
# First with default and not bootstrapped smoothing kernel, 
# defined in `create_corrector` call
pid, stat, mcstat = corrector(data)
print("Default kernel, no bootstrapping: ")
print(pid)
print(stat)
print(mcstat)

# Can also pass the kernel argument to the corrector function itself
# Run corrector with bootstrapped default kernel (bootstrap seed = 1)
pid2, stat2, mcstat2 = corrector(data, kernel = ('default', 1) )
print("Default kernel, bootstrapping seed = 1: ")
print(pid2)
print(stat2)
print(mcstat2)
