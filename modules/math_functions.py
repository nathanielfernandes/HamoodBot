import sys
import io
from math import sqrt
from sympy import symbols, Eq, solve, parse_expr


chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbl = "abcdefghijklmnopqrstuvwxyz"


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


def calc_eq(equation):
    equation = equation.replace("^", "**").lower()
    try:
        solved = eval(str(parse_expr(equation)))
    except Exception:
        return "Invalid Input"

    return solved


def solve_eq(equation):
    equation = equation.replace("^", "**").lower()
    count = 0
    solved = []
    for i in symbl:
        if i in equation:
            count += 1
    try:
        if count > 0:
            sol = solve(Eq(parse_expr(equation), 0), dict=True)
            try:
                for solution in sol:
                    for k in solution.keys():
                        if count < 2:
                            solution[k] = round(eval(str(solution[k])), 3)
                        solved.append(f"{k} = {solution[k]}")
            except NameError:
                return "No Solution"
        else:
            solved = eval(str(parse_expr(equation)))
    except Exception:
        return "Invalid Input"

    return solved


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

