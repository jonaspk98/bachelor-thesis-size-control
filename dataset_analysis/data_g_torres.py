import io
import os

import pandas as pd
import requests

import config as cfg

if __name__ == '__main__':
    if not os.path.exists(cfg.GT_RECORD):
        url = "https://charvin.igbmc.science/yeastcycledynamics/Export-Yeast%20Cycle%20Dynamics.txt"
        print("Downloading data set... This might take some time.")
        s = requests.get(url).content
        os.mkdir(os.path.split(cfg.GT_RECORD)[0])
        df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep="\t")
        pd.to_pickle(df, cfg.GT_RECORD)
        print("Dataframe for record of Garmendia-Torres created under /data_sets/gt_cell_cycle_dynamics.pkl .")
    else:
        print("Record already exists.")
