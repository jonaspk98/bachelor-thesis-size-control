# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 09:24:08 2020

@author: jonas
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

import auxilary_tools as aux
from plots.pv_base_plotting import plot_vdiv_y_multi

if __name__ == "__main__":
    f = 2
    mpl.rc('axes', labelsize=8, titlesize=9, linewidth=0.8 / f, labelpad=4.0 / f, titlepad=6 / f)
    mpl.rc('lines', linewidth=1.5 / f, markersize=6 / f, markeredgewidth=1 / f)
    mpl.rc('xtick', labelsize=7)
    mpl.rc('xtick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick', labelsize=7)
    mpl.rc('legend', frameon=False, fontsize=7, borderpad=0.4 / f, labelspacing=0.5 / f, handlelength=2 / f,
           handleheight=0.7 / f, handletextpad=0.8 / f, borderaxespad=0.5 / f)
    mpl.rc('figure', figsize=(17 / 2.54, 5 / 2.54), dpi=300)
    sim_set_names = ["kg_vdiv_nodil_nHill_15_KHill_16.pkl", "kg_vdiv_nodil_plain.pkl"]
    load_fun = aux.get_load_df_fun("simulation_data/transformed_kg_vdiv_scans")
    sim_sets = [load_fun(name) for name in sim_set_names]
    plot_selections = ["SN_cCln3", "SN_cWhi3P", "SN_cWhi5", "SN_cCln12", "SN_Sbf_ac", "V_tot_fl"]
    rates = sim_sets[0].growth_rate
    fig, big_ax = plt.subplots()
    aux.clean_big_ax(big_ax)
    loc_dict = aux.get_inset_loc(2, 1, 0.08, 0)
    insets = [big_ax.inset_axes(loc_dict[key]) for key in loc_dict]
    for ax in insets:
        aux.clean_big_ax(ax)
    loc_dict1 = aux.get_inset_loc(2, 1, 0.02, 0)

    t_in = [insets[1].inset_axes(loc_dict1[key]) for key in loc_dict1]
    v_in = [insets[0].inset_axes(loc_dict1[key]) for key in loc_dict1]

    cb_ax, kw = mpl.colorbar.make_axes(big_ax, orientation="vertical", fraction=0.05, aspect=20, pad=0.005)
    desc = "G1 growth rate [fL/min]"
    for sim_set, t_ax, v_ax in zip(sim_sets, t_in, v_in):
        plot_vdiv_y_multi(sim_set, "v_trans", v_ax)
        plot_vdiv_y_multi(sim_set, "t_g1", t_ax)

    for ax in t_in + v_in:
        ax.set_xlim(right=50 + (10 - ax.get_xlim()[0]))

    for ax in [t_in[1], v_in[1]]:
        ax.tick_params(axis="y", labelcolor="none", left=True, right=False)
        ax.set_title("plain")
        ax.set_ylabel(None)

    for ax in [t_in[0], v_in[0]]:
        ax.set_title("stress-sensing")

    for ax in t_in:
        ax.set_ylim(bottom=0, top=160)
        ax.set_xticks([15, 30, 45])
        aux.make_grid(ax)

    for ax in t_in + v_in:
        ax.set_xlabel(None)

    for ax in insets:
        ax.set_xlabel("volume after division [fL]")

    for ax in v_in:
        ax.set_ylim(10, 65)
        ax.set_xticks([15, 30, 45])
        aux.make_grid(ax)

    cmap = plt.cm.coolwarm
    cb = aux.make_cb(cb_ax, rates, cmap, "vertical")
    cb.set_label(desc)
    cb.ax.tick_params()
    cb.ax.set_yticklabels(rates)
    insets[0].text(-0.13, 1.05, "(a)", transform=insets[0].transAxes, fontsize=12)
    insets[1].text(-0.13, 1.05, "(b)", transform=insets[1].transAxes, fontsize=12)

    # Whi5 conc = 2.5

    plt.savefig(r"C:\Users\jonas\Documents\BA-defense\vdiv_vg1_nodil.pdf", dpi=300, transparent=True, bbox_inches ="tight")
    plt.show()