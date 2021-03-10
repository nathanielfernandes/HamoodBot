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


def twos_compliment(og_binary):
    if og_binary[0] == "1":
        binary = og_binary.replace("0", "$").replace("1", "0").replace("$", "1")
        val = int(binary, 2) + 1
        n = "{0:b}".format(val)
        binary = og_binary[0] * (len(og_binary) - len(n)) + n
    else:
        binary = og_binary
    return binary


def ones_compliment(og_binary):
    if og_binary[0] == "1":
        temp = og_binary[1:]
        binary = og_binary[0] + temp.replace("0", "$").replace("1", "0").replace(
            "$", "1"
        )
    else:
        binary = og_binary

    return binary


def float_to_bin(num):
    num1 = bin(int(str(num).split(".")[0])).split("b")

    num2 = float("0" + "." + str(num).split(".")[1])
    sign = ["-", "1"] if num < 0 else ["", "0"]

    b = ""
    for i in range(23):
        num2 *= 2
        b += str(int(str(num2)[0]) // int(str(num2)[0])) if str(num2)[0] != "0" else "0"
        num2 = float("0" + "." + str(num2).split(".")[1])
        if num2 == 0:
            break

    if num1[1][0] == "1":
        exponent = len(num1[1]) - 1
        b2 = b
    else:
        exponent = b.find("1") - 1
        b2 = b[abs(int(exponent)) :]

    step1 = f"{sign[0]}{num1[1]}.{b})2"
    step2 = f"{sign[0]}{num1[1][0]}.{num1[1][1:]}{b2})2 x2^{exponent}"

    exponent_b = bin(exponent + 127).split("b")[1].zfill(8)

    bin_float = f"{num1[1][1:]}{b2}"

    step3 = f"{sign[1]} {exponent_b} {bin_float}{'0'*(23-len(bin_float))}"

    return f"Step 1 - Convert to target base: {step1}\nStep 2 - Normalize: {step2}\nStep 3 - Fill in bits: {step3}\n\n{num})10 => {step3}"


print(float_to_bin(-12.625))

