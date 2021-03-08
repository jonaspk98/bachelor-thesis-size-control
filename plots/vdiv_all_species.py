# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:38:47 2020

@author: jonas
"""

from typing import Callable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

import plots.auxilary_tools as aux


def get_plot_all_fun(selections: list, plot_selections: list, unit_dict: list) -> Callable[[list, float, object], list]:
    plot_ts_points = aux.get_plot_ts_points_fun(plot_selections)

    def plot_all(scan_res, tt, axes):
        scan_res = np.array(scan_res, dtype=object)
        param_vals, results, transition_states = scan_res.T
        cmap = mpl.cm.coolwarm

        for ax, sel in zip(axes, plot_selections):
            ax.set_ylabel(unit_dict[sel])

        for i, res in enumerate(results):
            color = aux.get_color(cmap, i, len(results))
            t = res["time"] / 60
            for ax, sel in zip(axes, plot_selections):
                ax.plot(t[t <= tt], res[sel][t <= tt], color=color)

        for sel in ["SN_Sbf_ac", "V_tot_fl"]:
            plot_ts_points(sel, transition_states, axes, cmap)

        idx = plot_selections.index("SN_Sbf_ac")
        axes[idx].plot([min(t), tt], [0.5, 0.5], color="grey", linestyle="--")
        handles = [Line2D([0], [0], linestyle="none", marker="o", markerfacecolor="none", markeredgecolor="black",
                          label="transition point")]
        axes[-1].legend(handles=handles, frameon=False, loc="lower right")

    return plot_all


def _get_param_val_fromV(scan_res):
    return [round(sr[0], 2) for sr in scan_res]


def plot_all_scan(scan_res, selections, plot_selections, unit_dict, param_val_fun, param_desc):
    plot_all = get_plot_all_fun(selections, plot_selections, unit_dict)
    lets = [x for x in "efcdab"]
    fig, big_ax = plt.subplots()
    aux.clean_big_ax(big_ax)
    inset_dict = aux.get_inset_loc(nx=2, ny=3, hs=0.1, vs=0.05)
    axes = [big_ax.inset_axes(inset_dict[key]) for key in inset_dict]
    big_ax.set_xlabel("time [min]")
    plot_all(scan_res, 80, axes)
    for ax, let in zip(axes, lets):
        if let in "bdf":
            ax.text(-0.17, 1.02, "({})".format(let), transform=ax.transAxes, fontsize=12)
        if let in "ace":
            ax.text(-0.25, 1.02, "({})".format(let), transform=ax.transAxes, fontsize=12)

    cb_ax, kw = mpl.colorbar.make_axes(big_ax, orientation="vertical", fraction=0.15, aspect=40, pad=0.02)
    param_vals = param_val_fun(scan_res)
    cmap = plt.cm.coolwarm
    cb = aux.make_cb(cb_ax, list(param_vals), cmap, "vertical")
    cb.set_label(param_desc)
    cb.ax.set_yticklabels(param_vals)

