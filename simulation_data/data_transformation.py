"""
The two dimensional parameter scans produce produce the trajectories for n(p_1)*n(p_2) simulations.
n(p_1), n(p_2) are the number of simulations per parameter. For the corresponding initial volume - transition volume
or initial volume - G1 duration plot, only the transition states are relevant.
transition states Volume and time relevant.
First param is growth-rate. Calculated from linear section of volume traces.
For every growth rate, initial volumes are varied
data frame v_ini, v_trans, delta_t
--> create nested dataframe
"""

import os as os
import pickle

import pandas as pd

import config
from plots.auxilary_tools import get_load_set_fun, get_rates_from_pV_scan

PATH_DIR = "simulation_data/param_scans"
TARGET_DIR = "simulation_data/transformed_kg_vdiv_scans"


def save_df(df: pd.DataFrame, file_name: str) -> None:
    with open(os.path.join(config.ROOT_DIR, TARGET_DIR, file_name), "wb") as f:
        pickle.dump(df, f)


def transform_data(scan_results: list) -> pd.DataFrame:
    ## get transition states, calculate growth rate
    growth_rates = get_rates_from_pV_scan(scan_results)
    data_frames = []
    for gr_set in scan_results:
        v_ini = []
        v_trans = []
        t_g1 = []
        for vol_set in gr_set:
            v_ini.append(vol_set[0])
            v_trans.append(vol_set[2]["V_tot_fl"])
            t_g1.append(vol_set[2]["time"])
        data_frames.append(pd.DataFrame({"v_ini": v_ini, "t_g1": t_g1, "v_trans": v_trans}))
    final_df = pd.DataFrame({"growth_rate": growth_rates, "volume_scans": data_frames})
    return final_df

def make_df(ini_dict):
    list_of_series = [ini_dict[key].append(pd.Series(index=["initial_volume"], data=[key])) for key in ini_dict]
    inital_values_df = pd.concat(list_of_series, axis=1).T
    return inital_values_df

def get_initial_state_for_kg_vdiv_scan(filenames):
    load_df_fun = get_load_set_fun("simulation_data/full_kg_vdiv_sets")
    sim_set_names = filenames
    sim_sets = [load_df_fun(name) for name in sim_set_names]

    gr1s = [simset[0] for simset in sim_sets]

    ini_dicts = [{res[0]: res[1].iloc[0] for res in results} for results in gr1s]
    ini_state_dfs = [make_df(ini_dict) for ini_dict in ini_dicts]
    for ini_state_df, name in zip(ini_state_dfs, ["kg_vdiv_nHill_10", "kg_vdiv_kpCln3_003"]):
        ini_state_df.to_csv(r"C:\Users\jonas\Development\g1-size-control\simulation_data\initials_states/" + name + "_ini_states.csv")

def transform_kg_vdiv_files():
    load_fun = get_load_set_fun(PATH_DIR)
    for file in os.listdir(os.path.join(config.ROOT_DIR, PATH_DIR)):
        if "kg_vdiv" in file:
            ds = load_fun(file)
            df = transform_data(ds)
            save_df(df, file)


