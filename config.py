# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:52:35 2020

@author: jonas
"""

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

SIM_DIST = os.path.join(ROOT_DIR, "simulation_data/random_dist")
SIM_SCAN = os.path.join(ROOT_DIR, "simulation_data/random_dist")
BIFURC = os.path.join(ROOT_DIR, "simulation_data/bifurcation_data")
MECHANICAL_SIZE_CONTROL_MOD = os.path.join(ROOT_DIR, "antimony_models/mechanicalSizeControl.txt")
SBFWHI5 = os.path.join(ROOT_DIR, "antimony_models/sbf_whi5_module.txt")
SIZE_REGULATION_MOD = os.path.join(ROOT_DIR, "antimony_models/size_regulation.txt")
GT_RECORD = os.path.join(ROOT_DIR, "data_sets/gt_cell_cycle_dynamics.pkl")

# selection for simulation
SELECTIONS = ["time", "SN_cCln3", "SN_cWhi3P", "SN_cWhi5", "SN_cCln12", "SN_Sbf_ac", "V_tot_fl", "SN_Sbft", "SN_cSbf",
              "SN_cWhi5P", "SN_cWhi5Sbf", "SN_cWhi5t", "SN_cSbft"]
# selection to show in plot
PLOT_SELECTIONS = ["SN_cCln3", "SN_cWhi3P", "SN_cWhi5", "SN_cCln12", "SN_Sbf_ac", "V_tot_fl"]
# dict for units fo y axis in plots
UNIT_DICT = {"SN_cCln3": "Cln3 conc. [a.u.]",
             "SN_cWhi3P": "Whi3P conc. [a.u.]",
             "SN_Sbf_ac": "$Sbf/Sbf_t$",
             "SN_cWhi5": "free Whi5 conc. [a.u.]",
             "SN_cCln12": "Cln12 conc. [a.u.]",
             "V_tot_fl": "volume [fL]",
             "SN_cWhi5t": "Whi5t conc [a.u.]",
             "SN_cWhi5Sbf": "Whi5Sbf conc [a.u.]",
             "SN_cSbft": "Sbf total conc [a.u.]",
             "SN_cWhi5P": "Whi5P conc. [a.u.]"}
