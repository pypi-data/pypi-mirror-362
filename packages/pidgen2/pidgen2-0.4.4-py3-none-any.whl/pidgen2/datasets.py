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

"""
Definitions of LHCb PID calibration datasets (ROOT files produced by WG productions). 
The ROOT files can contain several trees corresponding to different calibration samples. 
These dictionaries are used further in the definitions of calibration samples (see samples/ subdir). 
"""

run2_dir = "root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/LHCb/"
run1_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_Run1_conversion/Reco14_DATA/"
photon_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/photon/"

legacy_run2_pidcalib_datasets = {
  'MagDown_2018': [f"{run2_dir}/Collision18/PIDCALIB.ROOT/00109278/0000/00109278_{i:08}_1.pidcalib.root" for i in range(1, 403) ], 
  'MagUp_2018'  : [f"{run2_dir}/Collision18/PIDCALIB.ROOT/00109276/0000/00109276_{i:08}_1.pidcalib.root" for i in range(1, 429) ], 
  'MagDown_2017': [f"{run2_dir}/Collision17/PIDCALIB.ROOT/00106052/0000/00106052_{i:08}_1.pidcalib.root" for i in range(1, 372) ], 
  'MagUp_2017'  : [f"{run2_dir}/Collision17/PIDCALIB.ROOT/00106050/0000/00106050_{i:08}_1.pidcalib.root" for i in range(1, 314) ],
  'MagDown_2016': [f"{run2_dir}/Collision16/PIDCALIB.ROOT/00111825/0000/00111825_{i:08}_1.pidcalib.root" for i in range(1, 259) ], 
  'MagUp_2016'  : [f"{run2_dir}/Collision16/PIDCALIB.ROOT/00111823/0000/00111823_{i:08}_1.pidcalib.root" for i in range(1, 239) ], 
  'MagDown_2015': [f"{run2_dir}/Collision15/PIDCALIB.ROOT/00064785/0000/00064785_{i:08}_1.pidcalib.root" for i in range(1,  79) ], 
  'MagUp_2015'  : [f"{run2_dir}/Collision15/PIDCALIB.ROOT/00064787/0000/00064787_{i:08}_1.pidcalib.root" for i in range(1,  45) ], 
}

legacy_run2_pidcalib_jpsi2mumunopt_datasets = {
  'MagDown_2018': [f"{run2_dir}/Collision18/PIDCALIB.ROOT/00108870/0000/00108870_{i:08}_1.pidcalib.root" for i in range(1, 55) ],
  'MagUp_2018'  : [f"{run2_dir}/Collision18/PIDCALIB.ROOT/00108868/0000/00108868_{i:08}_1.pidcalib.root" for i in range(1, 64) ],
  'MagDown_2017': [f"{run2_dir}/Collision17/PIDCALIB.ROOT/00108864/0000/00108864_{i:08}_1.pidcalib.root" for i in range(1, 39) ],
  'MagUp_2017'  : [f"{run2_dir}/Collision17/PIDCALIB.ROOT/00108862/0000/00108862_{i:08}_1.pidcalib.root" for i in range(1, 33) ],
  'MagDown_2016': [f"{run2_dir}/Collision16/PIDCALIB.ROOT/00111667/0000/00111667_{i:08}_1.pidcalib.root" for i in range(1, 29) ],
  'MagUp_2016'  : [f"{run2_dir}/Collision16/PIDCALIB.ROOT/00111665/0000/00111665_{i:08}_1.pidcalib.root" for i in range(1, 25) ],
  'MagDown_2015': [f"{run2_dir}/Collision15/PIDCALIB.ROOT/00064785/0000/00064785_{i:08}_1.pidcalib.root" for i in range(1, 79) ],
  'MagUp_2015'  : [f"{run2_dir}/Collision15/PIDCALIB.ROOT/00064787/0000/00064787_{i:08}_1.pidcalib.root" for i in range(1, 45) ],
}

legacy_run2_b2jpsieek_stripping_datasets = {
  'MagDown_2015': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2015_electrons/pidcalib_BJpsiEE_MD.root'],
  'MagDown_2016': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2016_electrons/pidcalib_BJpsiEE_MD_TAGCUT.root'],
  'MagDown_2017': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2017_electrons/Turbo2017_B2KJpsiEE_MagDown.root'],
  'MagDown_2018': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2018_electrons/Turbo2018_B2KJpsiEE_MagDown.root'],
  'MagUp_2015'  : ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2015_electrons/pidcalib_BJpsiEE_MU.root'],
  'MagUp_2016'  : ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2016_electrons/pidcalib_BJpsiEE_MU_TAGCUT.root'], 
  'MagUp_2017'  : ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2017_electrons/Turbo2017_B2KJpsiEE_MagUp.root'], 
  'MagUp_2018'  : ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_2018_electrons/Turbo2018_B2KJpsiEE_MagUp.root'], 
}

run2_lb2lcpi_stripping_datasets = {
  'MagDown_2015': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp15_md.root'],
  'MagDown_2016': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp16_md.root'],
  'MagDown_2017': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp17_md.root'],
  'MagDown_2018': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp18_md.root'],
  'MagUp_2015': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp15_mu.root'],
  'MagUp_2016': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp16_mu.root'],
  'MagUp_2017': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp17_mu.root'],
  'MagUp_2018': ['root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/proton/lcpi_splot_exp18_mu.root']
}

converted_run1_pidcalib_datasets_dstar_k = {
  "MagUp_2011"   : [f"{run1_dir}/MagUp/DSt_K_MagUp_Strip21r1_{i}.root" for i in range(24) ], 
  "MagUp_2012"   : [f"{run1_dir}/MagUp/DSt_K_MagUp_Strip21_{i}.root" for i in range(72) ], 
  "MagDown_2011" : [f"{run1_dir}/MagDown/DSt_K_MagDown_Strip21r1_{i}.root" for i in range(35) ], 
  "MagDown_2012" : [f"{run1_dir}/MagDown/DSt_K_MagDown_Strip21_{i}.root" for i in range(71) ], 
}

converted_run1_pidcalib_datasets_dstar_pi = {
  "MagUp_2011"   : [f"{run1_dir}/MagUp/DSt_Pi_MagUp_Strip21r1_{i}.root" for i in range(24) ], 
  "MagUp_2012"   : [f"{run1_dir}/MagUp/DSt_Pi_MagUp_Strip21_{i}.root" for i in range(72) ], 
  "MagDown_2011" : [f"{run1_dir}/MagDown/DSt_Pi_MagDown_Strip21r1_{i}.root" for i in range(35) ], 
  "MagDown_2012" : [f"{run1_dir}/MagDown/DSt_Pi_MagDown_Strip21_{i}.root" for i in range(71) ], 
}

converted_run1_pidcalib_datasets_lam0_p = {
  "MagUp_2011"   : [f"{run1_dir}/MagUp/Lam0_P_MagUp_Strip21r1_{i}.root" for i in range(30) ], 
  "MagUp_2012"   : [f"{run1_dir}/MagUp/Lam0_P_MagUp_Strip21_{i}.root" for i in range(119) ], 
  "MagDown_2011" : [f"{run1_dir}/MagDown/Lam0_P_MagDown_Strip21r1_{i}.root" for i in range(41) ], 
  "MagDown_2012" : [f"{run1_dir}/MagDown/Lam0_P_MagDown_Strip21_{i}.root" for i in range(121) ], 
}

converted_run1_pidcalib_datasets_lblcmu_p = {
  "MagUp_2011"   : [f"{run1_dir}/MagUp/LcfB_P_MagUp_Strip21r1_{i}.root" for i in range(1) ], 
  "MagUp_2012"   : [f"{run1_dir}/MagUp/LcfB_P_MagUp_Strip21_{i}.root" for i in range(3) ], 
  "MagDown_2011" : [f"{run1_dir}/MagDown/LcfB_P_MagDown_Strip21r1_{i}.root" for i in range(2) ], 
  "MagDown_2012" : [f"{run1_dir}/MagDown/LcfB_P_MagDown_Strip21_{i}.root" for i in range(3) ], 
}

converted_run1_pidcalib_datasets_inclc_p = {
  "MagUp_2011"   : [f"{run1_dir}/MagUp/IncLc_P_MagUp_Strip21r1_{i}.root" for i in range(1) ], 
  "MagUp_2012"   : [f"{run1_dir}/MagUp/IncLc_P_MagUp_Strip21_{i}.root" for i in range(3) ], 
  "MagDown_2011" : [f"{run1_dir}/MagDown/IncLc_P_MagDown_Strip21r1_{i}.root" for i in range(2) ], 
  "MagDown_2012" : [f"{run1_dir}/MagDown/IncLc_P_MagDown_Strip21_{i}.root" for i in range(3) ], 
}

converted_run1_pidcalib_datasets_jpsimumu = {
  'MagUp_2011'   : [f"{run1_dir}/MagUp/Jpsi_Mu_MagUp_Strip21r1_{i}.root" for i in range(7+1) ], 
  'MagUp_2012'   : [f"{run1_dir}/MagUp/Jpsi_Mu_MagUp_Strip21_{i}.root" for i in range(81+1) ], 
  'MagDown_2011' : [f"{run1_dir}/MagDown/Jpsi_Mu_MagDown_Strip21r1_{i}.root" for i in range(11+1) ],
  'MagDown_2012' : [f"{run1_dir}/MagDown/Jpsi_Mu_MagDown_Strip21_{i}.root" for i in range(79+1) ], 
}

converted_run1_pidcalib_datasets_jpsimumunopt = {
  'MagUp_2011'   : [f"{run1_dir}/MagUp/Jpsi_Mu_nopt_MagUp_Strip21r1_2011.root"], 
  'MagUp_2012'   : [f"{run1_dir}/MagUp/Jpsi_Mu_nopt_MagUp_Strip21_2012.root"], 
  'MagDown_2011' : [f"{run1_dir}/MagDown/Jpsi_Mu_nopt_MagDown_Strip21r1_2011.root"],
  'MagDown_2012' : [f"{run1_dir}/MagDown/Jpsi_Mu_nopt_MagDown_Strip21_2012.root"], 
}

photon_run1_datasets_kstargamma = {
  "2011-2012" : [f"{photon_dir}/sWtd_run0_mode0.root"], 
}

photon_run1_datasets_kstargamma_partreco_type0 = {
  "2011-2012" : [f"{photon_dir}/sWtd_run0_mode0_partreco_type0.root"], 
}

photon_run1_datasets_kstargamma_partreco_type1 = {
  "2011-2012" : [f"{photon_dir}/sWtd_run0_mode0_partreco_type1.root"], 
}

photon_run2_datasets_kstargamma = {
  "2016" : [f"{photon_dir}/sWtd_run1_mode0.root"], 
  "2017" : [f"{photon_dir}/sWtd_run2_mode0.root"], 
  "2018" : [f"{photon_dir}/sWtd_run3_mode0.root"], 
}

photon_run2_datasets_kstargamma_partreco_type0 = {
  "2016" : [f"{photon_dir}/sWtd_run1_mode0_partreco_type0.root"], 
  "2017" : [f"{photon_dir}/sWtd_run2_mode0_partreco_type0.root"], 
  "2018" : [f"{photon_dir}/sWtd_run3_mode0_partreco_type0.root"], 
}

photon_run2_datasets_kstargamma_partreco_type1 = {
  "2016" : [f"{photon_dir}/sWtd_run1_mode0_partreco_type1.root"], 
  "2017" : [f"{photon_dir}/sWtd_run2_mode0_partreco_type1.root"], 
  "2018" : [f"{photon_dir}/sWtd_run3_mode0_partreco_type1.root"], 
}
