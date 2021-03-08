# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:06:26 2020

@author: jonas
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import roadrunner as rr
import tellurium as te

import config as cf
import plots.auxilary_tools as aux
import simulations.simulation_tools.aux_simu_tools as ast
import simulations.simulation_tools.model_reassignment_tools as mrt
from plots.vdiv_all_species import get_plot_all_fun
from simulations.simulation_tools.steady_state_finding import SteadyStateFinder
mpl.use("TkAgg")

def plot_all(scan_res, selections, plot_selections, unit_dict, tt=100):
    plot_all = get_plot_all_fun(selections, plot_selections, unit_dict)
    fig, big_ax = plt.subplots(figsize=(7, 7))
    aux.clean_big_ax(big_ax)
    inset_dict = aux.get_inset_loc(nx=2, ny=3, hs=0.1, vs=0.05)
    axes = [big_ax.inset_axes(inset_dict[key]) for key in inset_dict]
    big_ax.set_xlabel("time [min]")
    plot_all(scan_res, tt, axes)
    cb_ax, kw = mpl.colorbar.make_axes(big_ax, orientation="vertical", fraction=0.15, aspect=40, pad=0.02)
    param_vals = [round(sr[0], 2) for sr in scan_res]
    cmap = plt.cm.coolwarm
    cb = aux.make_cb(cb_ax, list(param_vals), cmap, "vertical")
    cb.set_label("volume after division [fL]")
    cb.ax.set_yticklabels(param_vals)


def volume_scan(mod, selections, ia_dict, rules_dict, vol_range: np.ndarray, ss_finder, ss_param_dict: dict,
                new_pars=None):
    if new_pars is None:
        new_pars = {}
    vol_scan_res = []
    for p in vol_range:
        mod.resetToOrigin()
        ss_selections = ["Cln3", "Whi3P", "Sbf", "Whi5", "Cln12", "Whi5Sbf", "Whi5P", "Whi3"]

        new_pars["r_os_0"] = ast.get_os_rad(p, 0.3)
        ss_param_dict["V"] = p
        ss_param_dict["kpCln12"] = 0
        steady_state_dict = ss_finder.get_steady_states(ss_param_dict, ss_selections)
        for key in steady_state_dict:
            model_key = "SN_" + key + "0"
            new_pars[model_key] = steady_state_dict[key]
        mod = mrt.set_model_params(mod, new_pars)
        mod = mrt.reassign_model(mod, ia_dict, rules_dict)
        mod.variable_step_size = True
        mod.integrator.relative_tolerance = 1e-10
        res = mod.simulate(0, 10000, 10000, selections=selections)
        res = ast.namedArray_to_df(res, selections)
        param_val = p
        transition_state = ast.get_transition_state(res)
        vol_scan_res.append([param_val, res, transition_state])
    return vol_scan_res


def simulate_vscan(vol_range: np.ndarray, selections, ss_param_dict: dict):
    model = te.loada(cf.MECHANICAL_SIZE_CONTROL_MOD)
    ss_finder = SteadyStateFinder(cf.SIZE_REGULATION_MOD)
    ia_dict, rules_dict = mrt.get_ia_and_rules(model)
    return volume_scan(model, selections, ia_dict, rules_dict, vol_range, ss_finder=ss_finder,
                       ss_param_dict=ss_param_dict)


if __name__ == "__main__":
    ### 
    rr.Logger.setLevel(2)
    # selection for simulation
    selections = cf.SELECTIONS
    # selection to show in plot
    plot_selections = cf.PLOT_SELECTIONS
    # dict for units fo y axis in plots
    sel_unit_dict = cf.UNIT_DICT

    ss_param_dict = {"V": 20, "stress": 0, "dV": 0, "kPhWhi5": 0, "kpCln3h": 0, "Whi50": 65}

    param_range = np.linspace(10, 50, 8)
    scan_res = simulate_vscan(param_range, selections, ss_param_dict)
    plot_all(scan_res, selections, plot_selections, sel_unit_dict, tt=100)
    plt.show()