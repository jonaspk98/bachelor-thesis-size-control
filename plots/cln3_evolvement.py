# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 16:25:33 2020

@author: jonas
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

import auxilary_tools as aux


def get_param_vals(scans):
    return [round(scan[0], 2) for scan in scans[0]]


def plot_quant(ax, label, scan, tt=40):
    results = [sample[1] for sample in scan]
    cmap = plt.cm.coolwarm
    for i, res in enumerate(results):
        color = aux.get_color(cmap, i, len(results))
        t = res.time / 60
        t_red = t[t <= tt]
        ax.plot(t_red, res[t <= tt][label], color=color)


if __name__ == "__main__":
    f = 2
    mpl.rc('axes', labelsize=8, titlesize=9, linewidth=0.8 / f, labelpad=4.0 / f, titlepad=6 / f)
    mpl.rc('lines', linewidth=1.5 / f, markersize=8 / f, markeredgewidth=1.5 / f)
    mpl.rc('xtick', labelsize=8)
    mpl.rc('xtick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick', labelsize=8)
    mpl.rc('legend', frameon=False, fontsize=7, borderpad=0.4 / f, labelspacing=0.5 / f, handlelength=2 / f,
           handleheight=0.7 / f, handletextpad=0.8 / f, borderaxespad=0.5 / f)
    mpl.rc('figure', figsize=(17 / 2.54, 8 / 2.54), dpi=300)

    names = [1, 10, 100]
    full_names = ["n_hill_" + str(name) + ".pkl" for name in names]

    scans = [aux.load_set(name) for name in full_names]

    fig, big_ax = plt.subplots()
    aux.clean_big_ax(big_ax)
    gs = aux.loc(nrows=2, ncols=3, hs=0.013, vs=0.02, width_ratios=(1 / 3, 1 / 3, 1 / 3), height_ratios=(1 / 2, 1 / 2))
    row_axes = [[big_ax.inset_axes(gs[k, i]) for i in range(gs.shape[1])] for k in range(gs.shape[0])]
    labels = ["SN_cCln3", "SN_cWhi3P"]

    for axes, label in zip(row_axes, labels):
        for ax, scan in zip(axes, scans):
            plot_quant(ax, label, scan)

    vols = get_param_vals(scans)
    cb_ax, kw = mpl.colorbar.make_axes(big_ax, fraction=0.15, aspect=20, pad=0.02)
    cb = aux.make_cb(ax=cb_ax, values=vols, cmap=plt.cm.coolwarm, orientation="vertical")
    cb.set_label("volume after division [fL]")
    cb.ax.set_yticklabels(vols)

    for i, axes in enumerate(row_axes):
        for k, ax in enumerate(axes):
            if i != 0:
                ax.set_xticklabels([])
                ax.set_xlabel(None)
            if i == 0:
                ax.set_xlabel("time [min]")

            if k != 0:
                ax.set_yticklabels([])
                ax.set_ylabel(None)
            if (i == 1) & (k == 0):
                ax.set_ylabel("Whi3P [a.u./fL]")
            if (i == 0) & (k == 0):
                ax.set_ylabel("Cln3 [a.u./fL]")

    for ax, name in zip(row_axes[1], names):
        ax.set_title("$n_H=$" + str(name))
        ax.set_ylim(-0.1, 4.7)
    for ax, name in zip(row_axes[0], names):
        ax.set_ylim(-0.05, 0.85)

    plt.show()
