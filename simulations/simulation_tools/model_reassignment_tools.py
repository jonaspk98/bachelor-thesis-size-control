# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:38:56 2020

@author: jonas
"""

import libsbml
import numpy as np


def _clean_exp_str(exp: str) -> str:
    symbols = "()/*^+-,"
    for sym in symbols:
        exp = exp.replace(sym, " ")
    return exp


def recalc_osmo_amount(p_dict, rules_dict, ia_dict):
    new_vol = recalc_assignment(rules_dict["V_tot_fl"], p_dict, ia_dict, rules_dict)
    return p_dict["[c_i]"] * new_vol * 1e-15


def _get_symb_from_clean_string(clean_exp):
    symb_list = clean_exp.split(" ")
    return [x for x in symb_list if (x != "") and (not x.isdigit())]


def get_symbols_from_math(exp: str) -> list:
    return _get_symb_from_clean_string(_clean_exp_str(exp))


def _get_sbml_rule_dict(sbml_model):
    return {rule.getId(): libsbml.formulaToString(rule.getMath()) for rule in sbml_model.getListOfRules() if
            rule.isAssignment()}


def _get_sbml_allrules_dict(sbml_model):
    return {rule.getId(): libsbml.formulaToString(rule.getMath()) for rule in sbml_model.getListOfRules()}


def _get_sbml_ini_dict(sbml_model):
    return {ini.getId(): libsbml.formulaToString(ini.getMath()) for ini in sbml_model.getListOfInitialAssignments()}


def get_ia_and_rules(model):
    sbml = model.getSBML()
    sbml_document = libsbml.readSBMLFromString(sbml)
    sbml_model = sbml_document.getModel()
    return _get_sbml_ini_dict(sbml_model), _get_sbml_rule_dict(sbml_model)


def set_model_params(model, param_dict: dict):
    for key in param_dict:
        model[key] = param_dict[key]
    return model


def recalc_assignment(ia_exp, p_dict: dict, ia_dict, rules: dict):
    math_dict = {"pi": np.pi, "pow": pow}
    p = {}
    for sym in set(get_symbols_from_math(ia_exp)):
        if sym in rules.keys():
            p[sym] = recalc_assignment(rules[sym], p_dict, ia_dict, rules)
        elif sym in ia_dict.keys():
            p[sym] = recalc_assignment(ia_dict[sym], p_dict, ia_dict, rules)
        else:
            p[sym] = eval(sym, p_dict, math_dict)
    return eval(ia_exp, p, math_dict)


def reassign_model(model, ia_dict: dict, rules_dict: dict):
    p_dict = get_model_parameters_as_dict(model)
    for key in ia_dict:
        model[key] = recalc_assignment(ia_dict[key], p_dict, ia_dict, rules_dict)
    if "c_i" in model.keys():
        model["c_i"] = recalc_osmo_amount(p_dict, rules_dict, ia_dict)
    return model


def starts_ends_w(string: str, startswith: tuple, endswith: tuple):
    return any([string.startswith(startswith), string.endswith(endswith)])


def get_model_parameters_as_dict(model):
    return {key: model[key] for key in model.iterkeys() if not starts_ends_w(key, ("init", "eigen"), ("'"))}
