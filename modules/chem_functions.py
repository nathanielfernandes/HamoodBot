import json
import os
import chempy
from chempy.units import default_units as u
from sympy import Matrix

elements = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/PubChemElements_all.json"
    )
)


def balance_equation(equation: str):
    equation = equation.replace(" ", "").split("->")
    reac, prod = equation[0].split("+"), equation[1].split("+")
    try:
        reac, prod = chempy.balance_stoichiometry(reac, prod)
    except ValueError as e:
        return e
    return dict(reac), dict(prod)


def format_equation(reac: dict, prod: dict):
    return "".join(
        [f"[{reac[r]}]{r} + " for r in reac.keys()]
        + [f" + [{prod[p]}]{p}" for p in prod.keys()]
    ).replace("+  +", "->")


def get_elements(compounds: list):
    dict1 = {}
    for c in compounds:
        try:
            dict2 = chempy.Substance.from_formula(c).composition
        except Exception:
            return
        dict1 = {
            key: dict1.get(key, 0) + dict2.get(key, 0)
            for key in set(dict1) | set(dict2)
        }

    return {
        f"{elements['Table']['Row'][i-1]['Cell'][1]}": dict1[i] for i in dict1.keys()
    }


def get_molar_mass(substance: str):
    try:
        return chempy.Substance.from_formula(substance).molar_mass(u)
    except Exception:
        return


def get_element_period(element):
    if element.isdigit():
        element = int(element)
    else:
        try:
            element = list((chempy.Substance.from_formula(element).composition).keys())[
                0
            ]
        except Exception:
            return

    return elements["Table"]["Row"][element - 1]["Cell"]
