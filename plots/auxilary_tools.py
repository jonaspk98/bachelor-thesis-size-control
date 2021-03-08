# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 09:29:20 2020

@author: jonas
"""

import os
import pickle
from typing import Callable

import matplotlib as mpl
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

import config


def get_load_set_fun(base_path: str) -> Callable[[str], list]:
    def load_set(name: str):
        with open(os.path.join(config.ROOT_DIR, base_path, name), "rb") as f:
            return pickle.load(f)

    return load_set


def get_load_df_fun(base_path: str) -> Callable[[str], pd.DataFrame]:
    def load_df(file_name: str) -> pd.DataFrame:
        return pd.read_pickle(os.path.join(config.ROOT_DIR, base_path, file_name))

    return load_df


def load_set(name):
    with open("C:/Users/jonas/Documents/Studium/Studienprojekt/simulation_data/" + name, "rb") as f:
        return pickle.load(f)


def clean_big_ax(ax):
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    ax.set_facecolor("none")


def _get_length(n: int, space: float, pad: float) -> float:
    if (n - 1) * space + 2 * pad >= 1:
        raise ValueError("sum of spaces is larger than axes")
    return (1 - ((n - 1) * space + 2 * pad)) / n


def get_inset_loc(nx: int, ny: int, hs: float, vs: float, pad=0.0):
    hl, vl = [_get_length(n, space, pad) for n, space in zip([nx, ny], [hs, vs])]
    xpos, ypos = pad, pad
    pos_dict = {}
    for y in range(ny):
        xpos = pad
        for x in range(nx):
            pos_dict[str(x) + str(y)] = [xpos, ypos, hl, vl]
            xpos += (hl + hs)
        ypos += (vl + vs)
    return pos_dict


def loc(nrows: int, ncols: int, hs: float, vs: float, width_ratios=None, height_ratios=None, pad=0.0):
    if not width_ratios:
        width_ratios = [1]
    if not height_ratios:
        height_ratios = [1]

    row_lens = _get_ratio_lens(nrows, vs, pad, height_ratios)
    col_lens = _get_ratio_lens(ncols, hs, pad, width_ratios)

    gs = np.ndarray(shape=(nrows, ncols), dtype=tuple)

    for nr in range(nrows):
        row_pos = (pad + sum(row_lens[:nr]) + nr * vs)
        for nc in range(ncols):
            col_pos = pad + sum(col_lens[:nc]) + nc * hs
            gs[nr, nc] = (col_pos, row_pos, col_lens[nc], row_lens[nr])
    return gs


def _get_ratio_lens(n: int, space: float, pad: float, ratios):
    if (n - 1) * space + 2 * pad >= 1:
        raise ValueError("sum of spaces is larger than axes")
    if n != len(ratios):
        raise IndexError("ratios must have lenght n")
    if round(sum(ratios), 5) != 1:
        raise ValueError("sum of ratios must be 1")
    return [(1 - ((n - 1) * space + 2 * pad)) * ratios[i] for i in range(n)]


def get_color(cmap, i, list_len):
    return cmap(float(i) / (list_len - 1))


def get_plot_ts_points_fun(plot_selections: list) -> Callable:
    def plot_ts_points(sel: str, transition_states: np.ndarray, axes, cmap):
        for i, ts in enumerate(transition_states):
            color = get_color(cmap, i, len(transition_states))
            idx = plot_selections.index(sel)
            if type(ts) != type(None):
                axes[idx].plot(ts[0] / 60, ts[idx + 1] if sel != "SN_Sbf_ac" else 0.5, linestyle="none", marker="o",
                               markeredgecolor="black", markerfacecolor=color, zorder=10)

    return plot_ts_points


def get_rates_from_p_scan(p_scan_results):
    return [_get_rate_p(p_scan_res) for p_scan_res in p_scan_results]


def get_V_from_p_scan(p_scan_results):
    return [_get_V_p(p_scan_res) for p_scan_res in p_scan_results]


def _get_V_p(p_scan_res):
    param_val, results, transition_states = p_scan_res
    return round(param_val, 1)


def _get_rate_p(p_scan_res):
    param_vals, results, transition_states = p_scan_res
    time = results["time"] / 60
    v = results["V_tot_fl"]
    idx = np.argmin(abs(time - 20))
    return round((v[idx] - v[0]) / time[idx], 2)


def get_rates_from_pV_scan(pV_scan_results):
    return [_get_rate_pV(vol_scan_res) for vol_scan_res in pV_scan_results]


def _get_rate_pV(vol_scan_res):
    param_vals, results, transition_states = vol_scan_res[0]
    time = results["time"] / 60
    v = results["V_tot_fl"]
    idx = np.argmin(abs(time - 20))
    return round((v[idx] - v[0]) / time[idx], 2)


def make_cb(ax, values, cmap, orientation):
    bounds = np.linspace(-0.5, -0.5 + len(values), len(values) + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, ticks=range(len(values)), orientation=orientation)


def make_grid(ax):
    ax.grid(which='major', alpha=0.5)
    ax.minorticks_on()
    ax.tick_params(axis="both", which='minor', color="none")


def _plot_scatter(ax, x, y, cmap):
    xy = np.vstack([x, y])
    density = gaussian_kde(xy)(xy)
    idx = np.argsort(density)
    density = density / max(density)
    x, y, density = x[idx], y[idx], density[idx]
    ax.scatter(x, y, c=cmap(density), s=1, zorder=0)


def make_scatter_cb(cb_ax):
    cmap = mpl.cm.viridis
    norm = mpl.colors.Normalize(0, 1)
    cb = mpl.colorbar.ColorbarBase(cb_ax, cmap=cmap, norm=norm, orientation="horizontal")
    cb.set_label("relative density")
    return cb
