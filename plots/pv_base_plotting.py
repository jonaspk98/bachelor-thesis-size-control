# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 09:49:15 2020

@author: jonas
"""

import matplotlib as mpl
import numpy as np
import pandas as pd

import plots.auxilary_tools as aux


def plot_vdiv_vstart_multi(scan_results, ax, plot_selections):
    cmap = mpl.cm.coolwarm
    ax.set_xlabel("volume after division [fL]")
    ax.set_ylabel("volume at START [fl]")
    ax.tick_params()
    for i, scan_res in enumerate(scan_results):
        color = aux.get_color(cmap, i, len(scan_results))
        _plot_vdiv_vg1(scan_res, ax, plot_selections, color)

    ax.plot([10, 60], [10, 60], color="grey", linestyle="--", label="identity")


def plot_vdiv_tg1_multi(scan_results, ax):
    cmap = mpl.cm.coolwarm
    ax.set_xlabel("volume after division [fL]")
    ax.set_ylabel("duration of G1 [min]")
    ax.tick_params()
    for i, scan_res in enumerate(scan_results):
        color = aux.get_color(cmap, i, len(scan_results))
        _plot_vdiv_tg1(scan_res, ax, color)


def plot_vdiv_y_multi(results: pd.DataFrame, df_column: str, ax):
    cmap = mpl.cm.coolwarm
    ax.set_xlabel("volume after division [fL]")
    ax.set_ylabel("duration of G1 [min]" if df_column == "t_G1" else "volume at START [fL]")
    ax.tick_params()
    for i, data in enumerate(results.iterrows()):
        _, row = data
        color = aux.get_color(cmap, i, results.shape[0])
        if df_column == "v_trans":
            ax.plot(row.volume_scans.v_ini, row.volume_scans.v_trans, color=color)
        elif df_column == "t_g1":
            ax.plot(row.volume_scans.v_ini, row.volume_scans.t_g1 / 60, color=color)
        else:
            raise ValueError("Not the right df_column. Choose between \"v_trans\" and \"t_g1\".")


def _plot_vdiv_tg1(scan_res, ax, color):
    scan_res = np.array(scan_res, dtype=object)
    param_vals, results, transition_states = scan_res.T
    transition_states = np.vstack(transition_states)
    ax.plot(param_vals, transition_states[:, 0] / 60, color=color)


def _plot_vdiv_vg1(scan_res, ax, plot_selections, color):
    scan_res = np.array(scan_res, dtype=object)
    param_vals, results, transition_states = scan_res.T
    transition_states = np.vstack(transition_states)
    idx = plot_selections.index("V_tot_fl")
    print(idx)
    ax.plot(param_vals, transition_states[:, idx + 1], color=color)
