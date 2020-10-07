import sys
import io
import os
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, sin, cos, tan, log
from sympy import symbols, Eq, solve, parse_expr, integrate

import signal
from contextlib import contextmanager

chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbl = "abcdefghijklmnopqrstuvwxyz"
colors = ["b", "g", "r", "c", "m"]
folder = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/tempImages"

# implemented from https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
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
    eq = eq.lower().replace("^", "**").replace("mod", "%")

    for i in range(len(eq) - 1):
        if eq[i].isdigit() and (eq[i + 1] in symbl or eq[i + 1] == "("):
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
    for i in range(len(eq) - 1):
        if eq[i + 1].isdigit() and (eq[i] in symbl or eq[i] == ")"):
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
    # for i in range(len(eq) - 1):
    #     if eq[i] in symbl and eq[i + 1] == "(":
    #         eq = eq[: i + 1] + "*" + eq[i + 1 :]
    for i in range(len(eq) - 1):
        if eq[i + 1] in symbl and eq[i] == ")":
            eq = eq[: i + 1] + "*" + eq[i + 1 :]
    # if NumP:
    #     eq = (
    #         eq.replace("sin", "np.sin")
    #         .replace("cos", "np.cos")
    #         .replace("tan", "np.tan")
    #         .replace("sqrt", "np.sqrt")
    #         .replace("log", "np.log")
    #     )
    return eq


def graph_eq(equations, title):
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


def twos_comp(number):
    answer = [numb for numb in number[::-1]]
    for i in range(len(answer)):
        answer[i] = "0" if answer[i] == "1" else "1"

    for i in range(len(answer)):
        if answer[i] == "1":
            answer[i] = "0"
        else:
            answer[i] = "1"
            break
    answer = "".join(answer)[::-1]

    return answer


def base_conversion(number, base1, base2):
    twosComp = False
    try:
        number, base1, base2 = str(number).upper(), int(base1), int(base2)
        if number[0] == "-":
            number = number[1:]
            if base1 == 2:
                number = twos_comp(number)
            if base2 == 2:
                twosComp = True

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

    if twosComp:
        answer = "1" + twos_comp(answer)

    return answer


def run_code(code):
    if "__" in code:
        return "Dangerous Request!"

    codeOut = io.StringIO()
    sys.stdout = codeOut

    try:
        with time_limit(1):
            exec(code, {})
    except Exception as e:
        sys.stdout = sys.__stdout__
        codeOut.close()
        return e

    out = codeOut.getvalue()
    sys.stdout = sys.__stdout__
    codeOut.close()

    return out
