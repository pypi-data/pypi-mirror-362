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

#import os
#os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

#from jax import config
#config.update("jax_enable_x64", True)  # double precision in jax by default
#config.update('jax_platform_name', 'cpu')

from warnings import simplefilter
import pandas as pd
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

import numpy as np
#np.errstate(invalid='ignore')
np.seterr(all='ignore')