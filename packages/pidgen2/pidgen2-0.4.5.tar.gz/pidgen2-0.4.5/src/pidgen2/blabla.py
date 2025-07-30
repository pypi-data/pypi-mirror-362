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
# Allows one to produce the PID response from the pt, eta and Ntracks values 
# stored in the numpy array of shape (N, 3) (where N is the number of candidates)

import numpy as np
from pidgen2.resampler import create_resampler

sample = "K_Dstar2Dpi"
dataset = "MagDown_2016"
calibvar = "MC15TuneV1_ProbNNK"
varseed = 1
kernel = ("default", 1)
scale = None

# Create resampler function initialised with the sample, dataset etc. 

resampler = create_resampler(
         sample = sample,           # Calibration sample (e.g. "pi_Dstar2Dpi")
         dataset = dataset,         # Dataset (e.g. "MagUp_2016")
         variable = calibvar,       # Calibration variable (e.g. "MC15TuneV1_ProbNNK")
         plot = True,               # If template needs to be created from scratch, produce control plots
         resampling_seed = varseed, # Random seed for resampling
         kernel = kernel,           # List of kernels and template seeds
         verbose = -1,              # Print debugging information
         nan = -1000.,              # Numerical value to substitute NaN, for regions w/o calibration data 
         scale = scale,             # Scale factors for input data 
         local_storage = "./templates/",  # Directory for local template storage, used when the template is not available in 
                                          # the global storage on EOS. 
      )

# Create the numpy structure for 4 tracks 
# (the last track is intentionally outside of the kinematic region)
pt = [1000., 2000., 3000., 1.]
eta = [3.5, 4.5, 2.5, 0.]
ntr = [100., 300., 200., 1.]

data = np.array([pt, eta, ntr], dtype = float).T

print(data)

# Run resampler on the numpy array. 
# The output is two 1D arrays of length N, 
#   pid : resampled PID response
#   stat : per-event statistics of the calibration sample

pid, stat = resampler(data)

print(pid)
print(stat)
