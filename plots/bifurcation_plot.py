# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 18:33:09 2020

@author: jonas
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import auxilary_tools as aux
import config as cf


def make_cb(ax, values, cmap, orientation):
    bounds = np.linspace(-0.5, -0.5 + len(values), len(values) + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, ticks=range(len(values)), orientation=orientation)


def load_data(name) -> dict:
    info_list = name.split("_")
    descs = ["free_param", "scan_param", "scan_val"]
    data_dict = dict(zip(descs, info_list))
    data_dict["df"] = pd.read_pickle(cf.BIFURC + "/" + name + ".pkl")
    return data_dict


def get_plot_data(df, free_param):
    df["Sbf"] = df["Sbf"] / 1.1
    lp_inds = list(df[df["LP"]].index)
    inds = lp_inds + [len(df) - 1]
    li = 0
    plot_lists = []
    print(inds)
    for ind in inds:
        print(ind)
        plot_dict = {
            "x": df[free_param][li:ind + 1],
            "y": df["Sbf"][li:ind + 1],
            "s": df.loc[ind - 1, "stability"]
        }
        plot_lists.append(plot_dict)
        li = ind
    return plot_lists


def get_tpoint(df, free_param):
    lp_inds = list(df[df["LP"]].index)
    if len(lp_inds) < 2:
        raise IndexError("Not enough limit points")
    tind = lp_inds[0]
    aoi = df[df[free_param] > df[free_param][tind]]
    if len(aoi) > 0:
        idx = min(aoi.index)
        y0, y1 = df["Sbf"][idx - 1], df["Sbf"][idx]
        x0, x1 = df[free_param][idx - 1], df[free_param][idx]
        xr = df[free_param][tind]
        y_fin = (y1 - y0) / (x1 - x0) * (xr - x0) + y0
        return [xr, df["Sbf"][tind], y_fin]


def cs(limit, size):
    return size * (limit[1] - limit[0])


if __name__ == "__main__":
    f = 2
    mpl.rc('axes', labelsize=8, titlesize=9, linewidth=0.8 / f, labelpad=4.0 / f, titlepad=10 / f)
    mpl.rc('lines', linewidth=2 / f)
    mpl.rc('xtick', labelsize=8)
    mpl.rc('xtick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick', labelsize=8)
    mpl.rc('legend', frameon=False, fontsize=8, borderpad=0.4 / f, labelspacing=0.5 / f, handlelength=2 / f,
           handleheight=0.7 / f, handletextpad=0.8 / f, borderaxespad=0.5 / f)
    mpl.rc('figure', figsize=(17 / 2.54, 5 / 2.54), dpi=300)
    names = [["Cln3_V_15", "Cln3_V_30", "Cln3_V_45"],
             ["V_Cln3_0", "V_Cln3_0.5", "V_Cln3_1"],
             ["V_fac_1", "V_fac_10", "V_fac_100"]
             ]

    fig, big_ax = plt.subplots()
    aux.clean_big_ax(big_ax)
    dset_list = [[load_data(n) for n in name] for name in names]
    n = 16
    big_gs = aux.loc(2, 1, 0, 0.1, height_ratios=[(n - 1) / n, 1 / n])
    small_gs = aux.loc(1, 3, 0.02, 0, width_ratios=[1 / 3, 1 / 3, 1 / 3])
    two_axes = [big_ax.inset_axes(big_gs[i, 0]) for i in range(big_gs.shape[0])]
    d_axes, cb_axes = [[two_ax.inset_axes(small_gs[0, i]) for i in range(small_gs.shape[1])] for two_ax in two_axes]
    for ax in two_axes:
        aux.clean_big_ax(ax)

    labels = ["volume [fL]", "Cln3 [a.u./fL]", "Cln12 prod. factor"]
    unit_dict = {"Cln3": "Cln3 [a.u./fL]", "V": "volume [fL]"}
    limits = [(-0.05, 2.5), (-1.5, 61.5), (-1.5, 61.5)]
    for dset, d_ax, cb_ax, label, limit in zip(dset_list, d_axes, cb_axes, labels, limits):
        scan_vals = []
        cmap = plt.cm.coolwarm

        for i, data_dict in enumerate(dset):
            color = aux.get_color(cmap, i, len(dset))
            df = data_dict["df"]
            free_param = data_dict["free_param"]
            scan_vals.append(data_dict["scan_val"])
            for plt_dict in get_plot_data(df, free_param):
                ls_dict = {"N": ":", "S": "-"}
                d_ax.plot(plt_dict["x"], plt_dict["y"], ls_dict[plt_dict["s"]], color=color)
                try:
                    tp = get_tpoint(df, free_param)
                    d_ax.arrow(tp[0], tp[1], 0, tp[2] - tp[1], length_includes_head=True, head_width=cs(limit, 0.02),
                               head_length=0.1, alpha=0.7, linewidth=1.5 / f, facecolor=color, edgecolor="black",
                               zorder=5)
                    d_ax.plot((tp[0]), (tp[1]), marker="o", mec="black", mfc=color, ms=4, zorder=10)
                except IndexError:
                    continue
        cb = make_cb(cb_ax, scan_vals, cmap, "horizontal")
        cb.ax.set_xticklabels(scan_vals)
        cb.set_label(label)
        cb.ax.xaxis.set_label_position('top')
        d_ax.set_xlabel(unit_dict[free_param])
        d_ax.set_xlim(limit)

    for i, ax in enumerate(d_axes):
        if i != 0:
            ax.set_yticklabels([])
        else:
            ax.set_ylabel("free Sbf")

    handles = [
        mpl.lines.Line2D([0], [0], linestyle="none", marker="o", ms=4, mfc="none", mec="black", label="critical point")]
    d_axes[2].legend(handles=handles)

    for ax, let in zip(cb_axes, "abc"):
        ax.text(0.0, 1.8, "({})".format(let), transform=ax.transAxes, fontsize=12)
