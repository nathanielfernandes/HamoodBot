c310 = {
    "SETHI": [[21, 24, 29], ["op", "rd", "op2", "imm22"]],
    "Branch": [[21, 24, 28], ["op", "cond", "op2", "disp22"]],
    "CALL": [[29], ["op", "disp30"]],
    "Arithmetic1": [
        [4, 12, 13, 18, 24, 29],
        ["op", "rd", "op3", "rs1", "i", "00000000", "rs2"],
    ],
    "Arithmetic2": [[12, 13, 18, 24, 29], ["op", "rd", "op3", "rs1", "i", "simm13"],],
    "Memory1": [
        [4, 12, 13, 18, 24, 29],
        ["op", "rd", "op3", "rs1", "i", "00000000", "rs2"],
    ],
    "Memory2": [[12, 13, 18, 24, 29], ["op", "rd", "op3", "rs1", "i", "simm13"],],
}


def arrange(code: str, positions: list):
    spaces = positions[0] + [31]
    values = positions[1]
    code = code[::-1]
    j = 0
    new_code = ""
    for i in range(len(code)):
        if i == spaces[j]:
            new_code += code[i] + " "
            j += 1
        else:
            new_code += code[i]

    new_code = new_code[::-1].strip().split()

    top = []
    for i in range(len(new_code)):
        n = lambda x: int(len(x) / 2)
        if len(values[i]) != len(new_code[i]):
            top.append(
                ((n(new_code[i]) - n(values[i])) * " ")
                + values[i]
                + (
                    (
                        n(values[i])
                        + (
                            1
                            if (len(new_code[i]) in (5, 7) and len(values[i]) != 3)
                            else 0
                        )
                    )
                    * " "
                )
            )
        else:
            top.append(values[i])

    return " ".join(top) + "\n" + " ".join(new_code)


codes = {
    "010000": "addcc",
    "010001": "andcc",
    "010010": "orcc",
    "010110": "orncc",
    "100110": "srl",
    "111000": "jmpl",
    "000000": "ld",
    "000100": "st",
    "0001": "be",
    "0101": "bcs",
    "0110": "bneg",
    "0111": "bvs",
    "1000": "ba",
}


def get_inst(ops):
    get_op = lambda op: ops[1][ops[0].index(op)]
    if "op3" in ops[0]:
        ins = f"op3 = '{codes[get_op('op3')]}'"
    elif "cond" in ops[0]:
        ins = f"cond = '{codes[get_op('cond')]}'"
    else:
        ins = ""

    return ins


def format(content):
    content = content.replace(" ", "")
    if "\n" not in content:
        contents = [content]
    else:
        contents = content.split("\n")
    i = 1
    text = []

    for content in contents:
        if content[0] == "0":
            if content[1] == "0":
                if content[7] == "1":
                    form = "SETHI"
                else:
                    form = "Branch"
            else:
                form = "CALL"
        else:
            if content[1] == "0":
                if content[18] == "0":
                    form = "Arithmetic1"
                else:
                    form = "Arithmetic2"
            else:
                if content[18] == "0":
                    form = "Memory1"
                else:
                    form = "Memory2"

        a = arrange(content, c310[form]).split("\n")
        ops = [a[0].split(), a[1].split()]

        ins = get_inst(ops)

        t = f"{i}{(21-len(form + ' Format: '))*' '}{form} Format: "
        text.append(
            f"{' '*(22-len(ins)-6)}{ins}{' '*6}{a[0]}\n{(22-len(t))*' '}{t}{a[1]}"
        )
        i += 1
    s = f'\n{60*"-"}\n'
    # output = "```java\n" + s.join(text) + "\n```"

    output = s.join(text)
    return output


b = "00000010100000000000000000000101"
bruh = format(b)
print(bruh)

