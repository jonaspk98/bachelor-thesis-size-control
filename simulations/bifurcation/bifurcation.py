# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:41:44 2020

@author: jonas
"""

import os as os

import PyDSTool as dst
import pandas as pd
import tellurium as te

import config as cfg


def set_params_from_dict(obj, param_dict):
    for key in param_dict:
        obj[key] = param_dict[key]


def get_steady_states(param_dict) -> dict:
    rr = te.loada(cfg.SBFWHI5)
    set_params_from_dict(rr, param_dict)
    selections = ["Whi5P", "Sbf", "Cln12"]
    res = rr.simulate(0, 20000, 2, selections=selections)
    return {sel: res[sel][-1] for sel in selections}


def get_pycont(param_dict):
    DSargs = dst.args(name='Whi5_Sbf_module')
    # parameters
    DSargs.pars = {"kasSW": 1.67,
                   "kdisSW": 1.67e-4,
                   "kPhWhi5": 1e-3,
                   "kDphWhi5": 5e-4,
                   "fac": 58,
                   "kdCln12": 0.0015,
                   "Sbft": 1.1,
                   "Whi50": 65,
                   "V": 20,
                   "Cln3": 1.0
                   }

    DSargs.varspecs = {'Cln12': 'kdCln12*fac*Sbf/Sbft - kdCln12*Cln12',
                       'Sbf': '-kasSW*(Whi50/V+Sbf-Sbft-Whi5P)*Sbf + (kdisSW + kPhWhi5*(Cln12+Cln3))*(Sbft-Sbf)',
                       'Whi5P': '(kPhWhi5*(Cln12+Cln3))*(Whi50/V-Whi5P) - kDphWhi5*Whi5P',
                       }

    set_params_from_dict(DSargs.pars, param_dict)
    DSargs.ics = get_steady_states(param_dict)
    ode = dst.Generator.Vode_ODEsystem(DSargs)

    return dst.ContClass(ode)


def _sol_to_dict(sol):
    stability = [sol.labels["EP"][i]["stab"] for i in range(len(sol))]
    limit_inds = [i for i in sol.labels["LP"].keys()]
    lp_bools = [False for i in range(len(sol))]
    for i in limit_inds:
        lp_bools[i] = True
    data_dict = {key: sol[key] for key in sol.keys()}
    data_dict["stability"] = stability
    data_dict["LP"] = lp_bools
    return pd.DataFrame(data_dict)


def cont_sol_to_df(cont):
    return [_sol_to_dict(cont[lab].sol) for lab in cont.curves.keys()]


def save_dfs(dfs, names):
    for df, name in zip(dfs, names):
        pd.to_pickle(df, os.path.join(cfg.BIFURC, name))


def bifurk(cont, maxval, freepar):
    label = "EQ{}".format(len(cont.curves))
    PCargs = dst.args(name=label, type="EP-C")
    PCargs.freepars = [freepar]
    PCargs.MaxNumPoints = 50
    PCargs.StepSize = 1e-2
    PCargs.MaxStepSize = 0.5
    PCargs.LocBifPoints = ["LP"]
    PCargs.SaveEigen = True
    cont.newCurve(PCargs)
    while cont[label].parsdict[freepar] < maxval:
        cont[label].forward()


def _calc_bifurc_data(free_param, p_ini, scan_param, scan_val, max_val, name):
    param_dict = {free_param: p_ini, scan_param: scan_val}
    cont = get_pycont(param_dict)
    bifurk(cont, max_val, free_param)
    dfs = cont_sol_to_df(cont)
    save_dfs(dfs, [name])


def get_name(free_param, scan_param, scan_val):
    return "{}_{}_{}.pkl".format(free_param, scan_param, scan_val)


def bifurc_run(run: dict):
    free_param, p_ini, scan_param, scan_vals, max_val = [run[key] for key in run.keys()]

    for scan_val in scan_vals:
        name = get_name(free_param, scan_param, scan_val)
        _calc_bifurc_data(free_param, p_ini, scan_param, scan_val, max_val, name)


if __name__ == "__main__":
    runs = [{"freeparam": "V", "p_ini": 10, "scan_param": "Cln3", "scan_vals": [0, 0.5, 1], "max_val": 60},
            {"freeparam": "Cln3", "p_ini": 0.0, "scan_param": "V", "scan_vals": [15, 30, 45], "max_val": 2.5},
            {"freeparam": "V", "p_ini": 10, "scan_param": "fac", "scan_vals": [1, 10, 100], "max_val": 60}
            ]

    for run in runs:
        bifurc_run(run)
