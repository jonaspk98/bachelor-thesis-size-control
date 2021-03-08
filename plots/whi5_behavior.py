# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 09:08:52 2020

@author: jonas
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

import plots.auxilary_tools as aux


def plot_whi5(scan_res: list, tt: float, whi5_ax, v_ax, colors: list):
    scan_res = np.array(scan_res, dtype=object)
    param_vals, results, transition_states = scan_res.T

    param_vals = []
    for result in results:
        time = result["time"] / 60
        v = result["V_tot_fl"]
        idx = np.argmin(abs(time - 20))
        param_vals.append(round((v[idx] - v[0]) / time[idx], 2))

    for i, res in enumerate(results):
        print(len(res))
        color = colors[i]
        t = res["time"] / 60
        t_red = t[t <= tt]
        Whi5 = res["SN_cWhi5"]
        Whi5P = res["SN_cWhi5P"]
        Whi5Sbf = res["SN_cWhi5Sbf"]
        Whi5t = res["SN_cWhi5t"]

        whi5_ax.plot(t_red, (Whi5 / Whi5t)[t <= tt], color=color)
        whi5_ax.plot(t_red, (Whi5P / Whi5t)[t <= tt], color=color, linestyle="--")
        whi5_ax.plot(t_red, (Whi5Sbf / Whi5t)[t <= tt], color=color, linestyle=":")
        v_ax.plot(t_red, res["V_tot_fl"][t <= tt], color=color)

    for ts in transition_states:

        color = "black"
        t = ts[0] / 60
        if t < 60:
            whi5_ax.vlines(t, -0.1, 1.1, color=color, linestyle="-", alpha=0.4)
            v_ax.vlines(t, 15, 60, color=color, linestyle="-", alpha=0.4)


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
    mpl.rc('figure', figsize=(17 / 2.54, 8 / 2.54), dpi=300)
    names = ["Cln12prod.pkl", "Cln3prod.pkl", "kg.pkl"]
    full_names = ["scan_res_whi5_" + name for name in names]
    scans = [aux.load_set(name) for name in full_names]
    fig, (ax, ax1, ax2) = plt.subplots(1, 3)
    plt.subplots_adjust(wspace=0.05)
    for ax in fig.axes:
        aux.clean_big_ax(ax)
    gs = aux.loc(2, 1, 0, 0.02, height_ratios=[0.2, 0.8])
    v_axes = [ax.inset_axes(gs[0, 0]) for ax in fig.axes]
    whi5_axes = [ax.inset_axes(gs[1, 0]) for ax in fig.axes]

    tt = [60, 60, 60]
    colors = [("grey", "darkblue"), ("darkblue", "darkred"), ("darkblue", "darkred")]
    for scan_res, whi5_ax, v_ax, color_t, tt in zip(scans, whi5_axes, v_axes, colors, tt):
        plot_whi5(scan_res, tt=tt, whi5_ax=whi5_ax, v_ax=v_ax, colors=color_t)

    cbs = [mpl.colorbar.make_axes(ax, location="top", fraction=0.1, aspect=25, pad=0.06) for ax in fig.axes]
    cb_axes = [cb[0] for cb in cbs]

    ### kg scan
    kgs = aux.get_rates_from_p_scan(scans[2])
    kpCln3 = [scan[0] for scan in scans[1]]
    kpCln12 = ["off", "on"]
    vals = [kpCln12, kpCln3, kgs]

    cmaps = [mpl.colors.LinearSegmentedColormap.from_list("", list(color_t)) for color_t in colors]
    colorbars = [aux.make_cb(cb_ax, val, cmap, "horizontal") for cb_ax, val, cmap in zip(cb_axes, vals, cmaps)]
    labels = ["Cln12 positive feedback", "Cln3 prod. rate [a.u./s]", "G1 growth rate [fL/min]"]
    for cb, label, val in zip(colorbars, labels, vals):
        cb.set_label(label)
        cb.ax.set_xticklabels(val)
        cb.ax.xaxis.set_label_position('top')

    lets = "abc"
    xs = [-0.06, -0.06, -0.06]
    for ax, let, x in zip(whi5_axes, lets, xs):
        ax.set_xticklabels([])
        ax.set_ylim(-0.05, 1.05)
        ax.text(x, 1.18, "({})".format(let), transform=ax.transAxes, fontsize=12)
        aux.make_grid(ax)

    for ax in whi5_axes[1:]:
        ax.set_yticklabels([])
    for ax in v_axes[1:]:
        ax.set_yticklabels([])

    for ax in v_axes:
        ax.set_xlabel("time [min]")
        ax.set_ylim(19, 55)
        aux.make_grid(ax)

    whi5_axes[0].set_ylabel("fraction of $Whi5_t$")
    v_axes[0].set_ylabel("vol. [fL]")

    handles = [Line2D([0], [0], linestyle="-", color="black", label="Whi5"),
               Line2D([0], [0], linestyle="--", color="black", label="Whi5P"),
               Line2D([0], [0], linestyle=":", color="black", label="Whi5Sbf"),
               Line2D([0], [0], linestyle="-", color="black", alpha=0.4, linewidth=1, label="transition")]
    whi5_axes[0].legend(handles=handles, loc="upper left")

    plt.show()
