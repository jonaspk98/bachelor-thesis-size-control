# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 15:49:52 2021

@author: jonas
"""

from typing import Callable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

import plots.auxilary_tools as aux

def plot_whi3p_stress(axes, plot_selections, unit_dict, scan_res, tt):
    scan_res = np.array(scan_res, dtype=object)
    param_vals, results, transition_states = scan_res.T
    cmap = mpl.cm.coolwarm
    for res in results:
        res["stress"] = res["stress"] / 10e6
    for sel, ax in zip(plot_selections, axes):
        ax.set_ylabel(unit_dict[sel])

        for i, res in enumerate(results):
            color = aux.get_color(cmap, i, len(results))
            t = res["time"] / 60
            ax.plot(t[t <= tt], res[sel][t <= tt], color=color)
        for i, ts in enumerate(transition_states):
            if sel == "stress":
                ax.plot(ts["time"] / 60, ts[sel]/10e6, mfc=aux.get_color(cmap, i, len(results)), marker="o", mec="black",
                        zorder=5)
            else:
                ax.plot(ts["time"] / 60, ts[sel], mfc=aux.get_color(cmap, i, len(results)), marker="o", mec="black",
                        zorder=5)
    if "SN_Sbf_ac" in plot_selections:
        idx = plot_selections.index("SN_Sbf_ac")
        axes[idx].plot([min(t), tt], [0.5, 0.5], color="grey", linestyle="--")
        handles = [
            Line2D([0], [0], linestyle="none", marker="o", markerfacecolor="none", markeredgecolor="black",
                   label="transition point")]
        axes[-1].legend(handles=handles, frameon=False, loc="lower right")


def _get_param_val_fromV(scan_res):
    return [round(sr[0], 2) for sr in scan_res]


def plot_all_scan(scan_res, plot_selections, unit_dict, param_val_fun, param_desc):
    fig, big_ax = plt.subplots()
    aux.clean_big_ax(big_ax)
    inset_dict = aux.get_inset_loc(nx=2, ny=1, hs=0.08, vs=0.05)
    axes = [big_ax.inset_axes(inset_dict[key]) for key in inset_dict]
    big_ax.set_xlabel("time [min]")
    plot_whi3p_stress(axes, plot_selections, unit_dict, scan_res, 80)
    axes[0].set_ylabel(unit_dict[plot_selections[0]])


    #     if let in "bdf":
    #         ax.text(-0.17, 1.02, "({})".format(let), transform = ax.transAxes, fontsize=12)
    #     if let in "ace":
    #         ax.text(-0.25, 1.02, "({})".format(let), transform = ax.transAxes, fontsize=12)

    for ax in axes:
        aux.make_grid(ax)
    cb_ax, kw = mpl.colorbar.make_axes(big_ax, orientation="vertical", fraction=0.15, aspect=40, pad=0.02)
    param_vals = param_val_fun(scan_res)
    cmap = plt.cm.coolwarm
    cb = aux.make_cb(cb_ax, list(param_vals), cmap, "vertical")
    cb.set_label(param_desc)
    cb.ax.set_yticklabels(param_vals)
    axes[1].text(-0.15, 1.02, "({})".format("b"), transform=axes[1].transAxes, fontsize=12)
    axes[0].text(-0.25, 1.02, "({})".format("a"), transform=axes[0].transAxes, fontsize=12)


if __name__ == "__main__":
    f = 2
    mpl.rc('axes', labelsize=8, titlesize=9, linewidth=0.8 / f, labelpad=4.0 / f, titlepad=10 / f)
    mpl.rc('lines', linewidth=1.5 / f, markersize=8 / f, markeredgewidth=1.5 / f)
    mpl.rc('xtick', labelsize=8)
    mpl.rc('xtick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick', labelsize=8)
    mpl.rc('legend', frameon=False, fontsize=7, borderpad=0.4 / f, labelspacing=0.5 / f, handlelength=2 / f,
           handleheight=0.7 / f, handletextpad=0.8 / f, borderaxespad=0.5 / f)
    mpl.rc('figure', figsize=(15 / 2.54, 5 / 2.54), dpi=300)

    selections = ["time", "SN_cCln3", "SN_cWhi3P", "SN_cWhi5", "SN_cCln12", "SN_Sbf_ac", "V_tot_fl", "SN_Sbft",
                  "SN_cSbf", "SN_cWhi5P", "SN_cWhi5Sbf", "SN_cWhi5t", "SN_cSbft"]

    # dict for units fo y axis in plots
    unit_dict = {"SN_cCln3": "Cln3 [a.u./fL]",
                 "SN_cWhi3P": "Whi3P [a.u./fL]",
                 "SN_Sbf_ac": "$Sbf/Sbf_t$",
                 "SN_cWhi5": "free Whi5 [a.u./fL]",
                 "SN_cCln12": "Cln12 [a.u./fL]",
                 "V_tot_fl": "volume [fL]",
                 "SN_cWhi5t": "Whi5t [a.u./fL]",
                 "SN_cWhi5Sbf": "Whi5Sbf [a.u./fL]",
                 "SN_cSbft": "Sbf total [a.u./fL]",
                 "SN_cWhi5P": "Whi5P [a.u./fL]",
                 "stress": "[MPa]"}

    # scan_res = aux.load_set("standard_with_stress.pkl")
    # plot_selections = ["stress", "SN_cWhi3P"]
    scan_res = aux.load_set("n_hill_100_K_hill16_with_stress.pkl")
    plot_selections = ["SN_cWhi3P", "V_tot_fl"]
    #names = ["sbf_v", "whi5_whi5P", "cln3_cln12"]

    plot_all_scan(scan_res,
                  plot_selections,
                  unit_dict,
                  param_val_fun=aux.get_V_from_p_scan,
                  param_desc="volume after division [fL]")
    plt.show()
