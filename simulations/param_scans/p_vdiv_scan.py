# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 20:09:50 2020

@author: jonas
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import roadrunner as rr
import tellurium as te

import config as cf
import plots.auxilary_tools as aux
import plots.pv_base_plotting as pvb
import simulations.simulation_tools.model_reassignment_tools as mrt
from simulation_data.data_transformation import transform_data
from simulations.param_scans.volume_scan import volume_scan
from simulations.simulation_tools.steady_state_finding import SteadyStateFinder

mpl.use("TkAgg")


def plot_tv(result_df: pd.DataFrame, param_desc, vol_range, param_val_fun):
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    aux.clean_big_ax(ax)
    gs = aux.loc(nrows=1, ncols=2, hs=0.1, vs=0, width_ratios=(1 / 2, 1 / 2))
    tax, vax = [ax.inset_axes(gs[0, i]) for i in range(gs.shape[1])]
    pvb.plot_vdiv_y_multi(result_df, "v_trans", vax)
    pvb.plot_vdiv_y_multi(result_df, "t_g1", tax)
    pad = 0.05 * (vol_range[-1] - vol_range[0])
    vax.set_xlim(vol_range[0] - pad, vol_range[-1] + pad)
    cb_ax, kw = mpl.colorbar.make_axes(ax, fraction=0.15, aspect=25, pad=0.02)
    param_vals = param_val_fun(scan_results)
    cb = aux.make_cb(ax=cb_ax, values=param_vals, cmap=mpl.cm.coolwarm, orientation="vertical")
    cb.ax.set_yticklabels(param_vals)
    cb.set_label(param_desc)


def pv_scan(param: str, param_range, vol_range, ss_param_dict, mod, ia_dict, rules_dict, selections, ss_finder):
    param_scan_results = []
    for p in param_range:
        split = param.split("SN_")
        if len(split) == 2:
            ss_param_dict[split[-1]] = p
        new_pars = {param: p}
        param_scan_results.append(
            volume_scan(mod, selections, ia_dict, rules_dict, vol_range, ss_finder, ss_param_dict, new_pars=new_pars))
    return param_scan_results


def simulate_pv_scan(param, param_range, vol_range, ss_param_dict, selections):
    mod = te.loada(cf.MECHANICAL_SIZE_CONTROL_MOD)
    ss_finder = SteadyStateFinder(cf.SIZE_REGULATION_MOD)
    ia_dict, rules_dict = mrt.get_ia_and_rules(mod)
    return pv_scan(param, param_range, vol_range, ss_param_dict, mod, ia_dict, rules_dict, selections, ss_finder)


if __name__ == "__main__":
    ### 
    rr.Logger.setLevel(2)
    # selection for simulation
    selections = cf.SELECTIONS
    # dict for units fo y axis in plots
    sel_unit_dict = cf.UNIT_DICT

    ss_param_dict = {"V": 20, "stress": 0, "dV": 0, "kPhWhi5": 0, "kpCln3h": 0, "Whi50": 65}
    param = "k_nutrient_0"
    param_desc = "G1 growth rate [fL/min]"
    param_range = np.linspace(0.3e-16, 2.3e-16, 5)
    vol_range = np.linspace(10, 50, 30)
    scan_results = simulate_pv_scan(param, param_range, vol_range, ss_param_dict, selections)
    result_df = transform_data(scan_results)
    plot_tv(result_df, param_desc, vol_range, param_val_fun=aux.get_rates_from_pV_scan)
    plt.show()
