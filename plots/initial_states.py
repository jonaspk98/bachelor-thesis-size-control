# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:58:35 2020

@author: jonas

plots initial states used for the growth-rate, initial volumes scans.
Requires full simulation data which is not provided in Github, since the files are too big.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

import plots.auxilary_tools as aux

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
    mpl.rc('figure', figsize=(6 / 2.54, 12 / 2.54), dpi=300)
    mpl.rc('grid', linewidth=0.8 / 2.54)

    sim_set_names = ["kg_vdiv_nHill_10.pkl", "kg_vdiv_kpCln3_003.pkl"]
    sim_sets = [aux.load_set(name) for name in sim_set_names]

    gr1s = [simset[0] for simset in sim_sets]

    ini_dict = [{res[0]: res[1].iloc[0] for res in results} for results in gr1s]

    fig, axes = plt.subplots(2, 1)

    markers = ["o", "v", "p"]
    species = ["SN_cWhi5", "SN_cWhi5Sbf", "SN_cSbf"]
    for ax, idic in zip(axes, ini_dict):
        for marker, spec in zip(markers, species):
            for val in idic:
                ax.plot(val, idic[val][spec], linestyle="none", marker=marker, color="black")

    labels = ["Whi5", "Whi5Sbf", "free Sbf"]
    handles = [mpl.lines.Line2D([0], [0], linestyle="none", marker=m, color="black", label=l) for m, l in
               zip(markers, labels)]
    axes[0].legend(handles=handles)

    label = ("stress sensing model", "plain model")
    for ax, lab in zip(axes, label):
        ax.set_ylabel("concentrations [a.u/fL]")
        ax.set_xlabel("volume after division [fL]")
        ax3 = ax.twinx()
        ax3.set_yticks([])
        ax3.set_yticklabels([])
        ax3.set_ylabel(lab, fontsize=9)

    plt.show()
