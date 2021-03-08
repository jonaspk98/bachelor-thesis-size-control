# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 19:00:35 2020

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


def plot_all(param_desc, scan_res, selections, plot_selections, param_val_fun, unit_dict, tt=100):
    plot_all = get_plot_all_fun(selections, plot_selections, unit_dict)
    fig, big_ax = plt.subplots(figsize=(7, 7))
    aux.clean_big_ax(big_ax)
    inset_dict = aux.get_inset_loc(nx=2, ny=3, hs=0.1, vs=0.05)
    axes = [big_ax.inset_axes(inset_dict[key]) for key in inset_dict]
    big_ax.set_xlabel("time [min]")
    plot_all(scan_res, tt, axes)
    cb_ax, kw = mpl.colorbar.make_axes(big_ax, orientation="vertical", fraction=0.15, aspect=40, pad=0.02)
    param_vals = param_val_fun(scan_res)
    cmap = plt.cm.coolwarm
    cb = aux.make_cb(cb_ax, list(param_vals), cmap, "vertical")
    cb.set_label(param_desc)
    cb.ax.set_yticklabels(param_vals)


def p_scan(param, p_range, ss_finder, ia_dict, rules_dict, ss_param_dict, selections, mod, ini_volume):
    ss_selections = ["Cln3", "Whi3P", "Sbf", "Whi5", "Cln12", "Whi5Sbf", "Whi5P", "Whi3"]
    p_scan_res = []
    r_os = ast.get_os_rad(ini_volume, mod["r_b_0"])
    ss_param_dict["V"] = ast.vol(mod["r_b_0"] + r_os)

    for p in p_range:
        split = param.split("SN_")
        new_pars = {param: p}
        if len(split) == 2:
            ss_param_dict[split[-1]] = p
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
        transition_state = ast.get_transition_state(res)
        p_scan_res.append([p, res, transition_state])

    return p_scan_res


def simulate_pscan(param, param_range: np.ndarray, ini_volume, selections, ss_param_dict: dict):
    mod = te.loada(cf.MECHANICAL_SIZE_CONTROL_MOD)
    ss_finder = SteadyStateFinder(cf.SIZE_REGULATION_MOD)
    ia_dict, rules_dict = mrt.get_ia_and_rules(mod)
    return p_scan(param, param_range, ss_finder, ia_dict, rules_dict, ss_param_dict, selections, mod, ini_volume)


if __name__ == "__main__":
    rr.Logger.setLevel(2)

    # selection for simulation
    selections = cf.SELECTIONS
    # selection to show in plot
    plot_selections = cf.PLOT_SELECTIONS
    # dict for units fo y axis in plots
    sel_unit_dict = cf.UNIT_DICT

    ss_finder = SteadyStateFinder(cf.SIZE_REGULATION_MOD)
    ss_param_dict = {"V": 20, "stress": 0, "dV": 0, "kPhWhi5": 0, "kpCln3h": 0, "Whi50": 65}
    param_val_fun = aux.get_rates_from_p_scan
    param_desc = "G1 grwoth rate [fl/min]"
    scan_res = simulate_pscan("k_nutrient_0", np.linspace(0.3e-16, 2.3e-16, 5), 15, selections, ss_param_dict)
    plot_all(param_desc, scan_res, selections, plot_selections, param_val_fun, sel_unit_dict, tt=100)
