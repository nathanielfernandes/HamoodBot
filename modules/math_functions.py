import sys
import io
import os
import random
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, sin, cos, tan, log
from sympy import symbols, Eq, solve, parse_expr, integrate


chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbl = "abcdefghijklmnopqrstuvwxyz"
colors = ["b", "g", "r", "c", "m"]
folder = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/tempImages"


def format_eq(eq):
    eq = eq.lower().replace("^", "**").replace("mod", "%")
    return eq


def graph_eq(equations, title):
    equations = equations[:5]
    roots = []
    try:
        for equation in equations:
            eq = equation
            equation = format_eq(equation)

            x = np.array(range(-100, 100))
            y = eval(str(parse_expr(equation)))

            plt.title(title)

            roots.append(solve_eq(eq))

            plt.grid(alpha=0.5, linestyle="solid")
            plt.axhline(y=0, color="k", linewidth=0.5)
            plt.axvline(x=0, color="k", linewidth=0.5)

            plt.plot(x, y, label=f"y = {eq}", color=colors[equations.index(eq)])
            plt.legend()

            loc = f"{folder}/{equations}.jpg"

        plt.xlabel(f"Roots: {roots}")
        plt.savefig(loc, bbox_inches="tight")

    except Exception:
        return False, None

    plt.clf()
    return True, loc


def calc_eq(equation):
    equation = format_eq(equation)
    try:
        solved = eval(str(parse_expr(equation)))
    except Exception:
        return "Invalid Input"

    return solved


def solve_eq(equation):
    equation = format_eq(equation)
    solved = []

    try:
        sol = solve(Eq(parse_expr(equation), 0), dict=True)
        try:
            for solution in sol:
                for k in solution.keys():
                    solution[k] = round(eval(str(solution[k])), 3)
                    solved.append(f"{k} = {solution[k]}")
        except NameError:
            return "No Solution"
    except Exception:
        return "Invalid Input"

    return solved


def base_conversion(number, base1, base2):
    try:
        number, base1, base2 = str(number).upper(), int(base1), int(base2)
        if not 1 < base1 < 37 and not 1 < base2 < 37:
            return "<Invalid Entry>"
    except ValueError:
        return "<Invalid Entry>"

    for num in number:
        if num not in chars[:base1]:
            return "<Invalid Entry>"

    temp_number = 0
    for i in range(len(number)):
        temp_number += chars.index(number[::-1][i]) * base1 ** i

    answer = ""
    while temp_number >= 1:
        answer = chars[temp_number % base2] + answer
        temp_number = temp_number // base2

    return answer


def run_code(code):
    if "__" in code:
        return "Dangerous Request!"

    codeOut = io.StringIO()
    sys.stdout = codeOut

    try:
        exec(code, {})
    except Exception as e:
        sys.stdout = sys.__stdout__
        codeOut.close()
        return e

    out = codeOut.getvalue()
    sys.stdout = sys.__stdout__
    codeOut.close()

    return out
