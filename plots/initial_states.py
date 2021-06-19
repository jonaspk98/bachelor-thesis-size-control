# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:58:35 2020

@author: jonas

plots initial states used for the growth-rate, initial volumes scans.
Requires full simulation data which is not provided in Github, since the files are too big.
"""
from typing import Dict

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import plots.auxilary_tools as aux

def make_df(ini_dict):
    list_of_series = [ini_dict[key].append(pd.Series(index=["initial_volume"], data=[key])) for key in ini_dict]
    inital_values_df = pd.concat(list_of_series, axis=1).T
    return inital_values_df

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

    load_df_fun = aux.get_load_df_from_csv("simulation_data/initial_states")
    ini_state_df_names = ["kg_vdiv_nHill_10_ini_states.csv", "kg_vdiv_kpCln3_003_ini_states.csv"]
    ini_state_dfs = [load_df_fun(name) for name in ini_state_df_names]


    fig, axes = plt.subplots(2, 1)
    markers = ["o", "v", "p"]
    species = ["SN_cWhi5", "SN_cWhi5Sbf", "SN_cSbf"]
    for ax, ini_state_df in zip(axes, ini_state_dfs):
        for marker, spec in zip(markers, species):
            ax.plot(ini_state_df["initial_volume"], ini_state_df[spec], linestyle="none", marker=marker, color="black")

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
