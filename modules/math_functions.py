import sys
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

from urllib.parse import quote

carbon_data = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/carbon.json"
    )
)


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
    "raise",
    "SystemExit",
    "quit",
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


async def format_eq(eq):
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


async def graph_eq(equations, title):
    plt.clf()
    equations = equations[:5]
    roots = []
    ran = random.randint(5, 50)

    try:
        for equation in equations:
            if len(equation) > 1:
                ran = int(equation[1]) if 1 < int(equation[1]) < 101 else ran

            eq = equation
            equation = await format_eq(equation[0])

            x = np.array(np.arange(-1 * ran, ran, ran / 100))
            with time_limit(1):
                y = eval(str(parse_expr(equation)))

            plt.title(title)

            roots.append(await solve_eq(equation))

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


async def calc_eq(equation):
    equation = await format_eq(equation)
    try:
        with time_limit(1):
            solved = eval(str(parse_expr(equation)))
    except Exception:
        return "Invalid Input"

    return solved


async def solve_eq(equation):
    equation = await format_eq(equation)
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


async def base_conversion(number, base1, base2):
    try:
        return np.base_repr(int(number, base=base1), base2)
    except ValueError:
        return "Invalid Input"


async def get_derivative(equation, d):
    equation = await format_eq(equation)
    try:
        with time_limit(1):
            for i in range(d):
                equation = diff(equation)
        return str(equation)
    except Exception:
        return "Invalid Input"


async def run_code(code):
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
async def latex_to_text(formula):
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


async def carbon_code(code, random_theme=False):
    d = copy(carbon_data)

    theme = random.choice(
        [
            "material",
            "a11y-dark",
            "base-16",
            "duotone",
            "hopscotch",
            "lucario",
            "monokai",
            "synthwave-84",
            "panda",
            "paraiso",
            "dracula",
        ]
    )

    d.update({"code": code})
    d.update({"theme": theme})
    res = requests.post("https://carbonara.now.sh/api/cook/", json=d)

    save = (
        folder + "/" + "".join([str(random.randint(0, 9)) for i in range(9)]) + ".jpg"
    )

    with open(save, "wb") as handler:
        handler.write(res.content)

    return save


async def java_code(code):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US, en;q=0.9",
        "connection": "keep-alive",
        "accept-encoding": "gzip, deflate, br",
        "content-length": str(len(code)),
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "host": "www.compilejava.net",
        "origin": "https://www.compilejava.net",
        "referer": "https://www.compilejava.net/",
        "sec-ch-ua": '"Google Chrome";v="87", ""Not;A\\Brand";v="99", "Chromium";v="87"',
        "sec-ch-ua-mobile": "?1",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    data = {"code": code, "passargs": "", "respond": "respond"}

    response = requests.post("https://www.compilejava.net/", headers=headers, data=data)
    response = response.json()

    return response["execsout"]


# theme = "monokai"
# backgroundColor = "rgba(255,255,255,255)"
# # language = "auto"
# paddingVertical = "5px"
# paddingHorizontal = "5px"
# # exportsize = "3x"
# lineNumbers = "true"
# windowControls = "false"

# if random_theme:
#     theme = random.choice(
#         [
#             "material",
#             "a11y-dark",
#             "base-16",
#             "duotone",
#             "hopscotch",
#             "lucario",
#             "monokai",
#             "synthwave-84",
#             "panda",
#             "paraiso",
#             "dracula",
#         ]
#     )

# url = f"https://carbonnowsh.herokuapp.com/?code={quote(code)}&theme={theme}&backgroundColor={backgroundColor}&paddingVertical={paddingVertical}&paddingHorizontal={paddingHorizontal}&windowControls=false&lineNumbers=true"

# return url
