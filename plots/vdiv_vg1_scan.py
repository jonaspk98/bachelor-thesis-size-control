# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:07:48 2020

@author: jonas
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

import auxilary_tools as aux
from dataset_analysis.v_growthrate_stat import plot_scatt_tg1_torres, plot_scatt_vg1_torres
from plots.pv_base_plotting import plot_vdiv_y_multi

if __name__ == "__main__":
    f = 2
    mpl.rc('axes', labelsize=8, titlesize=9, linewidth=0.8 / f, labelpad=4.0 / f, titlepad=12 / f)
    mpl.rc('lines', linewidth=1.5 / f, markersize=6 / f, markeredgewidth=1 / f)
    mpl.rc('xtick', labelsize=7)
    mpl.rc('xtick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick', labelsize=7)
    mpl.rc('legend', frameon=False, fontsize=7, borderpad=0.4 / f, labelspacing=0.5 / f, handlelength=2 / f,
           handleheight=0.7 / f, handletextpad=0.8 / f, borderaxespad=0.5 / f)
    mpl.rc('figure', figsize=(17 / 2.54, 10 / 2.54), dpi=300)
    mpl.rc('grid', linewidth=0.8 / 2.54)
    load_fun = aux.get_load_df_fun("simulation_data/transformed_kg_vdiv_scans")
    sim_set_names = ["kg_vdiv_nHill_10.pkl", "kg_vdiv_kpCln3_003.pkl"]
    sim_sets = [load_fun(name) for name in sim_set_names]

    rates = sim_sets[0].growth_rate
    fig = plt.figure()

    gs = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[0.64, 0.36])
    big_ax, small_ax = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    fig.subplots_adjust(wspace=0.3)
    aux.clean_big_ax(big_ax)
    aux.clean_big_ax(small_ax)
    nx = 0.03
    ny = 0.02
    gs1 = aux.loc(2, 2, nx, ny, height_ratios=[1 / 2, 1 / 2], width_ratios=[1 / 2, 1 / 2])
    tg1_axes, vstart_axes = [[big_ax.inset_axes(gs1[k, i]) for i in range(gs1.shape[1])] for k in range(gs1.shape[0])]

    gs2 = aux.loc(2, 1, nx, ny, height_ratios=[1 / 2, 1 / 2])

    desc = "G1 growth rate [fL/min]"

    for i, sim_set in enumerate(sim_sets):
        plot_vdiv_y_multi(sim_set, "v_trans", vstart_axes[i])
        plot_vdiv_y_multi(sim_set, "t_g1", tg1_axes[i])

    cmap = mpl.pyplot.cm.coolwarm
    vstart_axes[0].set_title("stress sensing model")
    vstart_axes[1].set_title("plain model")

    cb_ax, kw = mpl.colorbar.make_axes(big_ax, orientation="vertical", fraction=0.1, aspect=30, pad=0.01)
    cb = aux.make_cb(cb_ax, list(rates), cmap, "vertical")
    cb.set_label(desc)
    cb.ax.tick_params()
    cb.ax.set_yticklabels(rates)

    for ax in vstart_axes:
        ax.set_xlabel(None)

        ax.legend(loc="lower right")
        ax.set_yticks([20, 30, 40, 50, 60])

        ax.set_xticklabels([])
    for ax in (vstart_axes[1], tg1_axes[1]):
        ax.set_ylabel(None)
        ax.set_yticklabels([])

    for ax in tg1_axes:
        ax.set_xticks([10, 20, 30, 40, 50])
        ax.set_xlabel(None)
        ax.set_ylim((-5.6913061870350035, 159.079))

    vstart_axes[0].text(-0.27, 1.05, "(a)", transform=vstart_axes[0].transAxes, fontsize=12)
    big_ax.set_xlabel("volume after division [fL]")

    ny = 0.025
    d_axes = [small_ax.inset_axes(gs2[i, 0]) for i in range(gs2.shape[0])]

    for ax in tg1_axes + vstart_axes + d_axes:
        aux.make_grid(ax)
    for ax in vstart_axes + [d_axes[1]]:
        ax.set_xticks([10, 20, 30, 40, 50])
        ax.set_xlim(9.1, 50.9)
        ax.set_ylim(15, 65)

    for ax in tg1_axes + [d_axes[0]]:
        ax.set_xticks([10, 20, 30, 40, 50])
        ax.set_xlim(9.1, 50.9)
        ax.set_ylim(-2.5, 159.079)

    small_ax.set_title("data (Garmendia-Torres et al.)")
    desc = "G1 growth rate [fL/min]"
    plot_scatt_vg1_torres(d_axes[1], cb_rel_ax=small_ax)
    plot_scatt_tg1_torres(d_axes[0])
    d_axes[0].set_ylim(top=159.079)
    d_axes[1].set_xlabel(None)
    d_axes[1].set_xticklabels([])
    d_axes[1].text(-0.55, 1.05, "(b)", transform=d_axes[1].transAxes, fontsize=12)
    plt.show()
