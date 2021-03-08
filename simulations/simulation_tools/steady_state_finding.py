# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:15:28 2020

@author: jonas
"""
import numpy as np
import tellurium as te

import simulations.simulation_tools.model_reassignment_tools as mrt


def clean_result(result):
    return max(result, 0)


vec_clean_result = np.vectorize(clean_result)


class SteadyStateFinder:
    def __init__(self, model_path: str):
        self.ss_dicts = []
        self.model = te.loada(model_path)
        self.ia_dict, self.rules_dict = mrt.get_ia_and_rules(self.model)
        self.set_integrator_opt()

    def set_integrator_opt(self):
        self.model.integrator.relative_tolerance = 1e-10

    def get_steady_states(self, params_val_dict: dict, selections: list) -> dict:
        self._setup_model(params_val_dict)
        res = self.model.simulate(0, 15000, 2, selections=selections)
        result = np.array(res[-1])
        result[result < 0] = 0
        ssdict = self._ss_to_dict(result, selections)
        self.ss_dicts.append(ssdict)
        return ssdict

    def _ss_to_dict(self, result, selections: list):
        return dict(zip(selections, result))

    def _setup_model(self, params_val_dict: dict):
        self.model.resetToOrigin()
        params_val_dict["pS"] = 1
        self.model = mrt.set_model_params(self.model, params_val_dict)
        self.model = mrt.reassign_model(self.model, self.ia_dict, self.rules_dict)
