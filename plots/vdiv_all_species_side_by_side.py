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


def get_plot_all_fun(unit_dict: list) -> Callable[[list, float, object], list]:
    def plot_all(scan_res_double, plot_selections, tt, axes_double):
        for scan_res, axes in zip(scan_res_double, axes_double):

            scan_res = np.array(scan_res, dtype=object)
            param_vals, results, transition_states = scan_res.T
            cmap = mpl.cm.coolwarm
            for sel, ax in zip(plot_selections, axes):
                ax.set_ylabel(unit_dict[sel])

                for i, res in enumerate(results):
                    color = aux.get_color(cmap, i, len(results))
                    t = res["time"] / 60
                    ax.plot(t[t <= tt], res[sel][t <= tt], color=color)
                for i, ts in enumerate(transition_states):
                    ax.plot(ts["time"] / 60, ts[sel], mfc=aux.get_color(cmap, i, len(results)), marker="o", mec="black",
                            zorder=5)

            if "SN_Sbf_ac" in plot_selections:
                idx = plot_selections.index("SN_Sbf_ac")
                axes[idx].plot([min(t), tt], [0.5, 0.5], color="grey", linestyle="--")
                handles = [
                    Line2D([0], [0], linestyle="none", marker="o", markerfacecolor="none", markeredgecolor="black",
                           label="transition point")]
                axes[-1].legend(handles=handles, frameon=False, loc="lower right")

    return plot_all


def _get_param_val_fromV(scan_res):
    return [round(sr[0], 2) for sr in scan_res]


def plot_all_scan(scan_res_double, plot_selections, unit_dict, param_val_fun, param_desc):
    plot_all = get_plot_all_fun(unit_dict)
    lets = [x for x in "ba"]
    fig, big_ax = plt.subplots()
    aux.clean_big_ax(big_ax)
    inset_dict = aux.get_inset_loc(nx=2, ny=2, hs=0.02, vs=0.05)
    st_axes = [big_ax.inset_axes(inset_dict[key]) for key in inset_dict if key[0] == "0"]
    sf_axes = [big_ax.inset_axes(inset_dict[key]) for key in inset_dict if key[0] == "1"]
    axes_double = [st_axes, sf_axes]
    big_ax.set_xlabel("time [min]")
    plot_all(scan_res_double, plot_selections, 80, axes_double)
    st_axes[1].set_title("stress sensing")
    sf_axes[1].set_title("plain")
    for ax in sf_axes:
        ax.set_ylabel(None)
        ax.set_yticklabels([])
    for ax, let in zip(st_axes, lets):
        ax.text(-0.25, 1.02, "({})".format(let), transform=ax.transAxes, fontsize=12)

    #     if let in "bdf":
    #         ax.text(-0.17, 1.02, "({})".format(let), transform = ax.transAxes, fontsize=12)
    #     if let in "ace":
    #         ax.text(-0.25, 1.02, "({})".format(let), transform = ax.transAxes, fontsize=12)

    for ax_st, ax_sf in zip(st_axes, sf_axes):
        y_lim = max(ax_st.get_ylim()[1], ax_sf.get_ylim()[1])
        ax_st.set_ylim(top=y_lim)
        ax_sf.set_ylim(top=y_lim)
        for ax in [ax_st, ax_sf]:
            aux.make_grid(ax)
    cb_ax, kw = mpl.colorbar.make_axes(big_ax, orientation="vertical", fraction=0.15, aspect=40, pad=0.02)
    param_vals = param_val_fun(scan_res_double[0])
    cmap = plt.cm.coolwarm
    cb = aux.make_cb(cb_ax, list(param_vals), cmap, "vertical")
    cb.set_label(param_desc)
    cb.ax.set_yticklabels(param_vals)


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
    mpl.rc('figure', figsize=(15 / 2.54, 10 / 2.54), dpi=300)

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
                 "SN_cWhi5P": "Whi5P [a.u./fL]"}

    scan_res_double = [aux.load_set("scan_res_vdiv_st.pkl")[0::3], aux.load_set("scan_res_vdiv_sf.pkl")[0::3]]
    plot_selections = [["SN_Sbf_ac", "V_tot_fl"], ["SN_cWhi5P", "SN_cWhi5"], ["SN_cCln12", "SN_cCln3"]]
    names = ["sbf_v", "whi5_whi5P", "cln3_cln12"]
    for plot_selections, name in zip(plot_selections, names):
        plot_all_scan(scan_res_double,
                      plot_selections,
                      unit_dict,
                      param_val_fun=aux.get_V_from_p_scan,
                      param_desc="volume after division [fL]")
    plt.show()
