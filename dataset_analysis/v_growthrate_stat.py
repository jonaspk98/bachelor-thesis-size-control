# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 19:31:22 2020

@author: jonas
"""

# -*- coding: utf-8 -*-


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
from matplotlib.lines import Line2D
from scipy.stats import gaussian_kde

import config as cfg


def get_xvals(bin_edges):
    size = bin_edges[1] - bin_edges[0]
    x_vals = [bin_edges[i] - size / 2 for i in range(1, len(bin_edges))]
    return x_vals


def make_cb_edge(ax, values, cmap, orientation):
    norm = mpl.colors.BoundaryNorm(values, cmap.N)
    return mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, ticks=values, orientation=orientation)


def get_intervals(gr, num):
    mean = np.mean(gr)
    std = np.std(gr)
    min_bound = max(0, mean - 2 * std)
    max_bound = mean + 2 * std
    vec = np.linspace(min_bound, max_bound, num + 1)
    return [[vec[i], vec[i + 1]] for i in range(num)]


def get_color(cmap, i, list_len):
    return cmap(float(i) / (list_len - 1))


def text_n(ax, i, n, bin_num):
    if i == 0:
        ax.text(0.5, -0.02, "n", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
                fontsize=9)
    x_pos = 0.56
    y_pos = 1 / bin_num * (i + 1 / 2)
    ax.text(x_pos, y_pos, n, horizontalalignment='center',
            verticalalignment='center', ha='center', rotation=90, fontsize=7, transform=ax.transAxes)


def plot_scatter(ax, x, y, cmap):
    xy = np.vstack([x, y])
    density = gaussian_kde(xy)(xy)
    idx = np.argsort(density)
    density = density / max(density)
    x, y, density = x[idx], y[idx], density[idx]
    ax.scatter(x, y, c=cmap(density), s=3, alpha=0.3, zorder=0)


def lin(x, m, n):
    return m * x + n


def count(arr: np.ndarray, val: int):
    count = 0
    for i in arr:
        if i == val:
            count += 1
    return count


def make_scatter_dist_plot(ax, x, y, rangeX, bins, color):
    stats, bin_edges, bin_numbers = st.binned_statistic(x, y, statistic="mean", bins=bins, range=rangeX)
    std = st.binned_statistic(x, y, statistic="std", bins=bins, range=rangeX)[0]
    x_vals = get_xvals(bin_edges)
    ax.plot(x_vals, stats, color=color, linestyle="-", marker="o", markersize=3, markeredgecolor=color,
            markerfacecolor="none")
    ax.fill_between(x=x_vals, y1=stats - std, y2=stats + std, color=color, alpha=0.05)
    ax.plot(x_vals, stats - std, linestyle="--", color=color, alpha=0.9, linewidth=0.5 / 2)
    ax.plot(x_vals, stats + std, linestyle="--", color=color, alpha=0.9, linewidth=0.5 / 2)


def make_hist(gr):
    fig, ax = plt.subplots()
    ax.hist(gr, 100, range=(-0.05, 2))
    ax.set_xlabel("growth rate [fL/min]")
    ax.set_ylabel("absolute frequenzy")
    ax.text(0.78, 0.9, "n = {}".format(len(gr)), transform=plt.gca().transAxes)


def plot_scatt_vg1_torres(ax, cb_rel_ax=None):
    data_set = pd.read_pickle(cfg.GT_RECORD)
    data_bud = data_set.loc[data_set["mother"] == "f"]
    data_bud = data_bud.loc[data_bud.strain == "WT"]
    gr = (data_bud["mub"]).to_numpy()
    data_bud = data_bud[gr >= 0]
    v_start = "vg1b"
    v_div = "vbirth"
    ivals = get_intervals(gr, 4)

    cb_vals = np.unique(np.hstack(ivals))
    cb_vals = [np.round(val, 2) for val in cb_vals]
    cmap = plt.cm.coolwarm
    cb_ax, kw = mpl.colorbar.make_axes(cb_rel_ax, orientation="vertical", fraction=0.2, aspect=30, pad=0.02)
    cb = make_cb_edge(cb_ax, cb_vals, cmap, "vertical")
    cb.set_label("G1 growth rate [fL/min]")
    ax.plot([12.5, 47.5], [12.5, 47.5], linestyle="--", color="grey", alpha=1, label="identity")

    n_used = 0
    ax.set_xlabel("volume after division [fL]")
    ax.set_ylabel("volume at START [fL]")
    for i, ival in enumerate(ivals):
        data_plot = data_bud.loc[np.logical_and(gr >= ival[0], gr < ival[1])]
        n_used += len(data_plot)
        color = get_color(cmap, i, len(ivals))
        x = data_plot[v_div].to_numpy()
        y = data_plot[v_start].to_numpy()

        text_n(cb_ax, i, len(data_plot), bin_num=4)
        make_scatter_dist_plot(ax, x, y, (10, 50), 8, color)
    handles = [Line2D([0], [0], linestyle="none", marker="o", markerfacecolor="none", markeredgecolor="black",
                      label="binned\nmeans"),
               Line2D([0], [0], linestyle="--", color="grey", label="identity")]
    ax.legend(handles=handles, loc="lower right")
    ax.text(0.03, 0.94, "$n_{{tot}}$={}".format(n_used), horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=8)


def plot_scatt_tg1_torres(ax):
    data_set = pd.read_pickle(cfg.GT_RECORD)
    data_bud = data_set.loc[data_set["mother"] == "f"]
    data_bud = data_bud.loc[data_bud.strain == "WT"]
    gr = (data_bud["mub"]).to_numpy()
    data_bud = data_bud[gr >= 0]
    tg1 = "tg1"
    v_div = "vbirth"
    ivals = get_intervals(gr, 4)

    cmap = plt.cm.coolwarm
    n_used = 0
    ax.set_xlabel("volume after division [fL]")
    ax.set_ylabel("duration of G1 [min]")
    for i, ival in enumerate(ivals):
        data_plot = data_bud.loc[np.logical_and(gr >= ival[0], gr < ival[1])]
        n_used += len(data_plot)
        color = get_color(cmap, i, len(ivals))

        x = data_plot[v_div].to_numpy()
        y = data_plot[tg1].to_numpy()

        make_scatter_dist_plot(ax, x, y, (10, 50), 8, color)

    handles = [Line2D([0], [0], linestyle="none", marker="o", markerfacecolor="none", markeredgecolor="black",
                      label="binned means"),
               ]

    ax.legend(handles=handles, loc="upper right")


if __name__ == "__main__":
    mpl.rc('axes', labelsize=12, titlesize=12)
    mpl.rc('xtick', labelsize=11)
    mpl.rc('ytick', labelsize=11)
    mpl.rc('legend', frameon=False, fontsize=12)
    mpl.rc('figure', dpi=300)
    data_set = pd.read_pickle(cfg.GT_RECORD)
    data_bud = data_set.loc[data_set["mother"] == "f"]
    data_bud = data_bud.loc[data_bud.strain == "WT"]
    gr = (data_bud["mub"]).to_numpy()
    data_bud = data_bud[gr >= 0]
    v_start = "vg1b"
    v_div = "vbirth"
    ivals = get_intervals(gr, 4)
    cb_vals = np.unique(np.hstack(ivals))
    cb_vals = [np.round(val, 2) for val in cb_vals]
    cmap = plt.cm.coolwarm
    fig = plt.figure(figsize=(5, 5))
    gs = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[9.5, 0.5])
    ax = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1])
    cb = make_cb_edge(ax1, cb_vals, cmap, "vertical")
    cb.set_label("G1 growth rate [fL/min]")
    ax.plot([12.5, 47.5], [12.5, 47.5], linestyle="--", color="grey", alpha=1, label="identity")

    n_used = 0
    for i, ival in enumerate(ivals):
        data_plot = data_bud.loc[np.logical_and(gr >= ival[0], gr < ival[1])]
        n_used += len(data_plot)
        color = get_color(cmap, i, len(ivals))

        x = data_plot[v_div].to_numpy()
        y = data_plot[v_start].to_numpy()
        ax.set_xlabel("volume after division [fL]")
        ax.set_ylabel("volume at START [fL]")
        text_n(ax1, i, len(data_plot), bin_num=4)
        make_scatter_dist_plot(ax, x, y, (10, 50), 8, color)
    handles = [Line2D([0], [0], linestyle="none", marker="o", markerfacecolor="none", markeredgecolor="black",
                      label="binned means"),
               Line2D([0], [0], linestyle="--", color="grey", label="identity")]

    ax.legend(handles=handles, frameon=False, loc="lower right")
    ax.text(0.03, 0.95, "$n_{{tot}}$={}".format(n_used), horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes)
    ax.set_ylim(bottom=10)

    fig.tight_layout()
    plt.show()
