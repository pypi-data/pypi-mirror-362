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
Definitions of LHCb PID MC datasets (ROOT files produced by WG productions). 
The ROOT files can contain several trees corresponding to different calibration samples. 
These dictionaries are used further in the definitions of calibration samples (see samples/ subdir). 
"""

run2sim09_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen/MC/Run2Sim09"
run2sim09_muon_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/mc/muon"
run1sim08_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen/MC/Run1Sim08"
run1sim09_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/mc/hadron"
run1sim09_muon_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/mc/muon"
photon_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/photon/"

lcmu_run1sim09_datasets = {
  'MagDown_2011' : [f"{run1sim09_dir}/tuple_lcmu_mc11_sim09_magdown.root"], 
  'MagUp_2011'   : [f"{run1sim09_dir}/tuple_lcmu_mc11_sim09_magup.root"], 
  'MagDown_2012' : [f"{run1sim09_dir}/tuple_lcmu_mc12_sim09_magdown.root"], 
  'MagUp_2012'   : [f"{run1sim09_dir}/tuple_lcmu_mc12_sim09_magup.root"], 
}

lcmu_run1sim08_datasets = {
  'MagDown_2011' : [f"{run1sim08_dir}/tuple_lcmu_mc11_magdown.root"], 
  'MagUp_2011'   : [f"{run1sim08_dir}/tuple_lcmu_mc11_magup.root"], 
  'MagDown_2012' : [f"{run1sim08_dir}/tuple_lcmu_mc12_magdown.root"], 
  'MagUp_2012'   : [f"{run1sim08_dir}/tuple_lcmu_mc12_magup.root"], 
}

dstar_run2sim09_datasets = {
  'MagDown_2018': [f"{run2sim09_dir}/tuple_dstar_mc18_magdown.root" ], 
  'MagUp_2018':   [f"{run2sim09_dir}/tuple_dstar_mc18_magup.root" ], 
  'MagDown_2017': [f"{run2sim09_dir}/tuple_dstar_mc17_magdown.root" ], 
  'MagUp_2017':   [f"{run2sim09_dir}/tuple_dstar_mc17_magup.root" ], 
  'MagDown_2016': [f"{run2sim09_dir}/tuple_dstar_mc16_magdown.root" ], 
  'MagUp_2016':   [f"{run2sim09_dir}/tuple_dstar_mc16_magup.root" ], 
  'MagDown_2015': [f"{run2sim09_dir}/tuple_dstar_mc15_magdown.root" ], 
  'MagUp_2015':   [f"{run2sim09_dir}/tuple_dstar_mc15_magup.root" ], 
}

lb2jpsipk_run2sim09_datsets = {
  'MagDown_2018': [f"{run2sim09_dir}/tuple_lb2jpsipk_md18.root" ], 
  'MagUp_2018':   [f"{run2sim09_dir}/tuple_lb2jpsipk_mu18.root" ], 
  'MagDown_2017': [f"{run2sim09_dir}/tuple_lb2jpsipk_md17.root" ], 
  'MagUp_2017':   [f"{run2sim09_dir}/tuple_lb2jpsipk_mu17.root" ], 
  'MagDown_2016': [f"{run2sim09_dir}/tuple_lb2jpsipk_md16.root" ], 
  'MagUp_2016':   [f"{run2sim09_dir}/tuple_lb2jpsipk_mu16.root" ], 
  'MagDown_2015': [f"{run2sim09_dir}/tuple_lb2jpsipk_md15.root" ], 
  'MagUp_2015':   [f"{run2sim09_dir}/tuple_lb2jpsipk_mu15.root" ], 
}

lb2lcmu_run2sim09_datsets = {
  'MagDown_2018': [f"{run2sim09_dir}/tuple_lcmu_mc18_magdown.root" ], 
  'MagUp_2018':   [f"{run2sim09_dir}/tuple_lcmu_mc18_magup.root" ], 
  'MagDown_2017': [f"{run2sim09_dir}/tuple_lcmu_mc17_magdown.root" ], 
  'MagUp_2017':   [f"{run2sim09_dir}/tuple_lcmu_mc17_magup.root" ], 
  'MagDown_2016': [f"{run2sim09_dir}/tuple_lcmu_mc16_magdown.root" ], 
  'MagUp_2016':   [f"{run2sim09_dir}/tuple_lcmu_mc16_magup.root" ], 
  'MagDown_2015': [f"{run2sim09_dir}/tuple_lcmu_mc15_magdown.root" ], 
  'MagUp_2015':   [f"{run2sim09_dir}/tuple_lcmu_mc15_magup.root" ], 
}

jpsimumu_run2sim09_datasets = {
  'MagDown_2018': [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc18_magdown.root" ], 
  'MagUp_2018':   [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc18_magup.root" ], 
  'MagDown_2017': [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc17_magdown.root" ], 
  'MagUp_2017':   [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc17_magup.root" ], 
  'MagDown_2016': [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc16_magdown.root" ], 
  'MagUp_2016':   [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc16_magup.root" ], 
  'MagDown_2015': [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc15_magdown.root" ], 
  'MagUp_2015':   [f"{run2sim09_muon_dir}/tuple_jpsimumu_sim09_mc15_magup.root" ], 
}

jpsimumu_run1sim09_datasets = {
  'MagDown_2012': [f"{run1sim09_muon_dir}/tuple_jpsik_mc12_sim09_magdown.root" ], 
  'MagUp_2012':   [f"{run1sim09_muon_dir}/tuple_jpsik_mc12_sim09_magup.root" ], 
  'MagDown_2011': [f"{run1sim09_muon_dir}/tuple_jpsik_mc11_sim09_magdown.root" ], 
  'MagUp_2011':   [f"{run1sim09_muon_dir}/tuple_jpsik_mc11_sim09_magup.root" ], 
}

jpsiee_run2sim09_datasets = {
  'MagDown_2018': [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc18_magdown_repro.root" ], 
  'MagUp_2018':   [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc18_magup_repro.root" ], 
  'MagDown_2017': [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc17_magdown_repro.root" ], 
  'MagUp_2017':   [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc17_magup_repro.root" ], 
  'MagDown_2016': [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc16_magdown_repro.root" ], 
  'MagUp_2016':   [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc16_magup_repro.root" ], 
  'MagDown_2015': [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc15_magdown_repro.root" ], 
  'MagUp_2015':   [f"{run2sim09_dir}/tuple_jpsiee_sim09_mc15_magup_repro.root" ], 
}

photon_run1sim09_datasets_kstargamma = {
  "2011-2012" : [f"{photon_dir}/mc_run0_mode0.root"], 
}

photon_run2sim09_datasets_kstargamma = {
  "2016" : [f"{photon_dir}/mc_run1_mode0.root"], 
  "2017" : [f"{photon_dir}/mc_run2_mode0.root"], 
  "2018" : [f"{photon_dir}/mc_run3_mode0.root"], 
}

