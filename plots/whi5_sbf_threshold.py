# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:10:57 2020

@author: jonas
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

import auxilary_tools as aux

load_set = aux.get_load_df_fun("simulation_data/random_dist")

if __name__ == "__main__":
    f = 2
    mpl.rc('axes', labelsize=8, titlesize=9, linewidth=0.8 / f, labelpad=4.0 / f, titlepad=3 / f)
    mpl.rc('lines', linewidth=1.5 / f, markersize=4 / f, markeredgewidth=1 / f)
    mpl.rc('xtick', labelsize=7)
    mpl.rc('xtick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick', labelsize=7)
    mpl.rc('legend', frameon=False, fontsize=9, borderpad=0.4 / f, labelspacing=1 / f, handlelength=2 / f,
           handleheight=1.4 / f, handletextpad=1.6 / f, borderaxespad=1 / f)
    mpl.rc('figure', figsize=(17 / 2.54, 20 / 2.54), dpi=300)

    names_st = ["trans_Vdep_noise_065_st_01.pkl", "trans_lin_065_st_01.pkl", "trans_Vdep_065_st_01.pkl"]
    names_sf = ["trans_Vdep_noise_065_sf_02.pkl", "trans_lin_065_sf.pkl", "trans_Vdep_065_sf.pkl"]
    dset_list = [[load_set(name) for name in names] for names in [names_st, names_sf]]

    fig, big_ax = plt.subplots()
    gs = aux.loc(2, 1, 0, 0.08, height_ratios=[1 / 2, 1 / 2])
    aux.clean_big_ax(big_ax)
    model_axes = [big_ax.inset_axes(gs[i, 0]) for i in range(gs.shape[0])]
    for ax in model_axes:
        aux.clean_big_ax(ax)

    gs_small = aux.loc(2, 3, 0.02, 0.02, width_ratios=[1 / 3 for i in range(3)], height_ratios=[1 / 2, 1 / 2])

    small_axes = [
        [[axes.inset_axes(gs_small[k, i]) for i in range(gs_small.shape[1])] for k in range(gs_small.shape[0])] for axes
        in model_axes]

    for model_ax, dsets in zip(small_axes, dset_list):
        for dset, t_ax, v_ax, in zip(dsets, model_ax[0], model_ax[1]):
            samples = [dset[dset.Whi5_ini < 1.1 * dset.vdiv], dset[dset.Whi5_ini >= 1.1 * dset.vdiv]]
            zorders = [2, 1]
            colors = ["red", "grey"]
            for sample, zorder, color in zip(samples, zorders, colors):
                v_ax.scatter(sample.vdiv, sample.vstart, zorder=zorder, color=color, alpha=0.5)
                t_ax.scatter(sample.vdiv, sample.time / 60, zorder=zorder, color=color, alpha=0.5)

    for ax, title, in zip(model_axes, ["stress sensing model", "plain model"]):
        twin_ax = ax.twinx()
        twin_ax.set_yticklabels([])
        aux.clean_big_ax(twin_ax)
        twin_ax.set_ylabel(title, fontsize=10)

    labels = ["initial Whi5 lower than Sbf conc.", "initial Whi5 higher than Sbf conc."]
    colors = ["red", "grey"]
    handles = [mpl.lines.Line2D([0], [0], marker="o", linestyle="none", mfc=color, mec=color, label=label) for
               label, color in zip(labels, colors)]

    titles = ["vol. dep. + noise", "lin. acc", "vol. dependent"]
    for j, model_ax in enumerate(small_axes):
        for i, axes in enumerate(model_ax):
            for k, ax in enumerate(axes):
                if i == 0 and k == 0:
                    ax.set_ylabel("duration of G1 [min]")
                if i == 1 and k == 0:
                    ax.set_ylabel("volume at START [fL]")

                if i == 1:
                    ax.set_xticklabels([])
                    ax.set_title(titles[k])
                if k != 0:
                    ax.set_yticklabels([])
                if i == 0:
                    ax.set_xlabel("volume after division [fL]")
                    ax.set_xlim(8, 85)
                    ax.set_ylim(-2.5, 152.5)

                if i == 1:
                    ax.set_ylim(12, 85)
                    ax.set_xlim(8, 82)
                ax.set_xticks([15, 30, 45, 60, 75])

    model_axes[1].legend(handles=handles, ncol=2, markerscale=2, bbox_to_anchor=(0, 1.05, 1, 0.1), loc="center")
    plt.show()
