# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 19:10:18 2020

@author: jonas
"""

import numpy as np
import pandas as pd
import pickle

def vol(r):
    return 4 / 3 * np.pi * r ** 3


def get_os_rad(V, r_b):
    r = rad(V)
    return r - r_b


def rad(V):
    return np.cbrt(3 / 4 / np.pi * V)


def get_transition_state(res):
    dif = abs(res["SN_Sbf_ac"] - 0.5)
    idx = dif.idxmin()
    return res.loc[idx]


def namedArray_to_df(namedArray, selections):
    data_dict = {sel: namedArray[sel] for sel in selections}
    return pd.DataFrame(data_dict)


def save(obj: list, path:str):
    with open(path, "wb") as f:
        pickle.dump(obj, f)

