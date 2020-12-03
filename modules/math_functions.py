import sys
import io
import os
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, sin, cos, tan, log
from sympy import symbols, Eq, solve, parse_expr, integrate, diff

import time, math, random

import signal
from contextlib import contextmanager

import pylab

chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbl = "abcdefghijklmnopqrstuvwxyz"
colors = ["b", "g", "r", "c", "m"]
folder = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/tempImages"
restricted = [
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
]


# This function was implemented from https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
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


def format_eq(eq):
    eq = (
        eq.lower()
        .replace("^", "**")
        .replace("mod", "%")
        .replace("sin", "[sin]")
        .replace("sqrt", "[sqrt]")
        .replace("cos", "[cos]")
        .replace("tan", "[tan]")
        .replace("log", "[log]")
        .replace("ln", "[ln]")
    ) + len(eq) * " "

    for i in range(len(eq) - 1):
        if eq[i].isdigit() and (eq[i + 1] in symbl or eq[i + 1] == "("):
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
        # for i in range(len(eq) - 1):
        elif eq[i + 1].isdigit() and (eq[i] in symbl or eq[i] == ")"):
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
        # for i in range(len(eq) - 1):
        elif eq[i] in symbl and eq[i + 1] == "(":
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
        # for i in range(len(eq) - 1):
        elif eq[i + 1] in symbl and eq[i] == ")":
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
        # for i in range(len(eq) - 1):
        elif eq[i] == ")" and eq[i + 1] == "(":
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
        # for i in range(len(eq) - 1):
        elif (
            eq[i] in symbl and eq[i + 1] == "[" or eq[i].isdigit() and eq[i + 1] == "["
        ):
            eq = eq[: i + 1] + "*" + eq[i + 1 :]

    eq = (
        eq.lower()
        .replace("[sin]", "sin")
        .replace("[sqrt]", "sqrt")
        .replace("[cos]", "cos")
        .replace("[tan]", "tan")
        .replace("[log]", "log")
        .replace("[ln]", "log")
        .replace(" ", "")
    )

    return eq


def graph_eq(equations, title):
    plt.clf()
    equations = equations[:5]
    roots = []
    ran = random.randint(5, 50)

    try:
        for equation in equations:
            if len(equation) > 1:
                ran = int(equation[1]) if 1 < int(equation[1]) < 101 else ran

            eq = equation
            equation = format_eq(equation[0])

            x = np.array(np.arange(-1 * ran, ran, ran / 100))
            with time_limit(1):
                y = eval(str(parse_expr(equation)))

            plt.title(title)

            roots.append(solve_eq(equation))

            plt.grid(alpha=0.5, linestyle="solid")
            plt.axhline(y=0, color="k", linewidth=0.5)
            plt.axvline(x=0, color="k", linewidth=0.5)

            plt.plot(x, y, label=f"y = {equation}", color=colors[equations.index(eq)])
            plt.legend()

            loc = f"{folder}/{equation}.jpg"

        plt.xlabel(f"Roots: {roots}")
        plt.savefig(loc, bbox_inches="tight")

    except Exception:
        return False, None

    plt.clf()
    return True, loc


def calc_eq(equation):
    equation = format_eq(equation)
    try:
        with time_limit(1):
            solved = eval(str(parse_expr(equation)))
    except Exception:
        return "Invalid Input"

    return solved


def solve_eq(equation):
    equation = format_eq(equation)
    solved = []

    try:
        sol = solve(Eq(parse_expr(equation), 0), dict=True)
        for solution in sol:
            for k in solution.keys():
                if "I" not in str(solution[k]):
                    solution[k] = round(eval(str(solution[k])), 3)
                    solved.append(f"{k} = {solution[k]}")
    except Exception:
        return "Invalid Input"

    if not solved:
        return "Could not Solve"
    else:
        return solved


def base_conversion(number, base1, base2):
    try:
        return np.base_repr(int(number, base1), base2)
    except ValueError:
        return "Invalid Input"


def get_derivative(equation, d):
    equation = format_eq(equation)
    try:
        with time_limit(1):
            for i in range(d):
                equation = diff(equation)
        return str(equation)
    except Exception:
        return "Invalid Input"


def run_code(code):
    for r in restricted:
        if r in code:
            return f"code cannot contain '{r}'", None

    # if "__" in code or "import" in code or "exit()" in code:
    #     return "code cannot contain include '__' or 'import' for safety reasons!", None

    codeOut = io.StringIO()
    sys.stdout = codeOut

    try:
        with time_limit(1):
            tic = time.perf_counter()
            exec(code, {"time": time, "math": math, "random": random, "numpy": np})
            toc = time.perf_counter()
    except Exception as e:
        sys.stdout = sys.__stdout__
        codeOut.close()
        return e, None

    out = codeOut.getvalue()
    sys.stdout = sys.__stdout__
    codeOut.close()

    return out, f"{toc-tic:0.6f}"


# implemented from https://stackoverflow.com/questions/14110709/creating-images-of-mathematical-expressions-from-tex-using-matplotlib
def latex_to_text(formula):
    formula = formula.replace("`", "")

    if formula[0] != "$":
        formula = "$" + formula
    if formula[-1] != "$":
        formula += "$"

    save = (
        folder + "/" + "".join([str(random.randint(0, 9)) for i in range(9)]) + ".png"
    )

    try:
        formula = r"{}".format(formula)
        fig = pylab.figure()
        text = fig.text(0, 0, formula)

        # Saving the figure will render the text.
        dpi = 300
        fig.savefig(save, dpi=dpi)

        # Now we can work with text's bounding box.
        bbox = text.get_window_extent()
        width, height = bbox.size / float(dpi) + 0.005
        # Adjust the figure size so it can hold the entire text.
        fig.set_size_inches((width, height))

        # Adjust text's vertical position.
        dy = (bbox.ymin / float(dpi)) / height
        text.set_position((0, -dy))

        # Save the adjusted text.
        fig.savefig(save, dpi=dpi)
    except Exception as e:
        return save, e

    plt.clf()
    plt.close()
    return save, None
