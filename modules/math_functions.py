#
import sys, re
import requests
import json
import io
import os
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, sin, cos, tan, log
from sympy import symbols, Eq, solve, parse_expr, integrate, diff
from copy import copy
import time, math, random

import signal
from contextlib import contextmanager

import pylab

from utils.helpers import to_async


def flatten(l, condition=lambda e: True, switch=lambda e: e) -> list:
    return [switch(e) for t in l for e in t if condition(e)]


COLORS = ("b", "g", "r", "c", "m")
RESTRICTED = (
    "exit",
    "__",
    "_",
    "import",
    "eval",
    "exec",
    "open",
    "file",
    "input",
    "execfile",
    "stdin",
    "builtins",
    "globals",
    "locals",
    "try",
    "except",
    "calloc",
    "malloc",
    "sleep",
    "raise",
    "SystemExit",
    "quit",
)


folder = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/temp"


# Implemented from https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutError("Timed Out! Code execution surpassed 1 second!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


EQF = re.compile(
    r"(?:(\)\()|(\)[a-zA-Z])[^a-z]|[^a-z]([a-zA-Z]\()|(\d\()|(\)\d)|(\)[a-z])|(\d[a-zA-Z])|[^a-z]([a-zA-Z]\d+))"
)


def format_eq(eq):
    eq = (
        eq.replace(" ", "")
        .replace("\n", "")
        .replace("[", "(")
        .replace("]", ")")
        .replace("^", "**")
        .replace("mod", "%")
    )
    for res in RESTRICTED:
        eq = eq.replace(res, "")

    stuff = EQF.findall(eq)
    to_replace = flatten(stuff, lambda e: e != "")

    for rep in to_replace:
        eq = eq.replace(rep, f"{rep[0]}*{rep[-1]}")

    return eq


def graph_eq(equations):
    plt.clf()
    equations = equations[:5]

    try:
        with time_limit(2):
            for equation in equations:
                eq = equation
                equation = format_eq(equation)

                x = np.array(np.arange(-100, 100, 0.1))

                y = eval(
                    str(parse_expr(equation)),
                    {
                        "sqrt": sqrt,
                        "sin": sin,
                        "cos": cos,
                        "tan": tan,
                        "log": log,
                        "x": x,
                    },
                )

                # plt.title(title)

                plt.grid(alpha=0.5, linestyle="solid")
                plt.axhline(y=0, color="k", linewidth=0.5)
                plt.axvline(x=0, color="k", linewidth=0.5)

                plt.plot(
                    x,
                    y,
                    label=f"y = {equation.replace('**', '^')}",
                    color=COLORS[equations.index(eq)],
                )
                plt.legend()
        buffer = io.BytesIO()
        plt.savefig(buffer, bbox_inches="tight")
        plt.clf()
        buffer.seek(0)
        return buffer
    except Exception as e:
        if isinstance(e, TimeoutError):
            return "Timed Out! Calculation exceeded 1 second!"
        return "Invalid Input"


def calc_eq(equation):
    equation = format_eq(equation)
    try:
        with time_limit(1):
            solved = eval(
                str(parse_expr(equation)),
                {"sqrt": sqrt, "sin": sin, "cos": cos, "tan": tan, "log": log},
            )
    except Exception as e:
        if isinstance(e, TimeoutError):
            return "Timed Out! Calculation exceeded 1 second!"
        return "Invalid Input"

    return solved


def solve_eq(equation):
    equation = format_eq(equation)
    solved = []

    try:
        with time_limit(1):
            sol = solve(Eq(parse_expr(equation), 0), dict=True)
            for solution in sol:
                for k in solution.keys():
                    if "I" not in str(solution[k]):
                        solution[k] = round(
                            eval(
                                str(solution[k]),
                                {
                                    "sqrt": sqrt,
                                    "sin": sin,
                                    "cos": cos,
                                    "tan": tan,
                                    "log": log,
                                },
                            ),
                            3,
                        )
                        solved.append(f"{k} = {solution[k]}")
    except Exception as e:
        if isinstance(e, TimeoutError):
            return "Timed Out! Calculation exceeded 1 second!"
        return "Invalid Input"

    return solved


def base_conversion(number, base1, base2):
    try:
        return np.base_repr(int(number, base=base1), base2)
    except ValueError:
        return "Invalid Input"


def get_derivative(equation, d):
    equation = format_eq(equation)
    try:
        with time_limit(1):
            for i in range(d):
                equation = diff(equation)
        return str(equation)
    except Exception as e:
        if isinstance(e, TimeoutError):
            return "Timed Out! Calculation exceeded 1 second!"
        return "Invalid Input"


# implemented from https://stackoverflow.com/questions/14110709/creating-images-of-mathematical-expressions-from-tex-using-matplotlib
def latex_to_text(formula):
    formula = formula.replace("`", "")

    if formula[0] != "$":
        formula = "$" + formula
    if formula[-1] != "$":
        formula += "$"

    try:
        buffer = io.BytesIO()
        formula = r"{}".format(formula)
        fig = pylab.figure()
        text = fig.text(0, 0, formula)

        # Saving the figure will render the text.
        dpi = 200
        fig.savefig(buffer, dpi=dpi)

        # Now we can work with text's bounding box.
        bbox = text.get_window_extent()
        width, height = bbox.size / float(dpi) + 0.005
        # Adjust the figure size so it can hold the entire text.
        fig.set_size_inches((width, height))

        # Adjust text's vertical position.
        dy = (bbox.ymin / float(dpi)) / height
        text.set_position((0, -dy))

        buffer = io.BytesIO()
        # Save the adjusted text.
        fig.savefig(buffer, dpi=dpi)

        buffer.seek(0)
        plt.clf()
        plt.close()
        return buffer

    except Exception as e:
        return e
