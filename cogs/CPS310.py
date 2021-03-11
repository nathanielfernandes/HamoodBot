import discord
from discord.ext import commands


class Cps310(commands.Cog):
    """310 Commands, dont cheat!"""

    def __init__(self, bot):
        self.bot = bot
        self.flag = False
        self.cheaters = []
        self.names = []
        self.c310 = {
            "SETHI": [[21, 24, 29], ["op", "rd", "op2", "imm22"]],
            "Branch": [[21, 24, 28], ["op", "cond", "op2", "disp22"]],
            "CALL": [[29], ["op", "disp30"]],
            "Arithmetic1": [
                [4, 12, 13, 18, 24, 29],
                ["op", "rd", "op3", "rs1", "i", "00000000", "rs2"],
            ],
            "Arithmetic2": [
                [12, 13, 18, 24, 29],
                ["op", "rd", "op3", "rs1", "i", "simm13"],
            ],
            "Memory1": [
                [4, 12, 13, 18, 24, 29],
                ["op", "rd", "op3", "rs1", "i", "00000000", "rs2"],
            ],
            "Memory2": [
                [12, 13, 18, 24, 29],
                ["op", "rd", "op3", "rs1", "i", "simm13"],
            ],
        }

        self.codes = {
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

        self.instructions = {
            "ld": f"\n[Description]: Load a register from main memory. The memory address must be aligned on a word boundary (that is, the address must be evenly divisible by 4). The address is computed by adding the contents of the register in the rs1 field to either the contents of the register in the rs2 field or the value in the simm13 field, as appropriate for the con- text.\n\n",
            "st": f"\n[Description]: Store a register into main memory. The memory address must be aligned on a word boundary. The address is computed by adding the contents of the register in the rs1 field to either the contents of the register in the rs2 field or the value in the simm13 field, as appropriate for the context. The rd field of this instruction is actually used for the source register.\n\n",
            "sethi": f"\n[Description]: Set the high 22 bits and zero the low 10 bits of a register. If the operand is 0 and the register is %r0, then the instruction behaves as a no-op (NOP), which means that no operation takes place.\n\nExample usage: sethi 0x304F15, %r1\n\n[Meaning]: Set the high 22 bits of %r1 to (304F15)16, and set the low 10 bits to zero.\n\nObject code: {self.format('00000011001100000100111100010101')}\n\n",
            "andcc": f"\n[Description]: Bitwise AND the source operands into the destination operand. The condition codes are set according to the result.\n\nExample usage: andcc %r1, %r2, %r3\n\n[Meaning]: Logically AND %r1 and %r2 and place the result in %r3.\n\nObject code: {self.format('10000110100010000100000000000010')}\n\n",
            "orcc": f"\n[Description]: Bitwise OR the source operands into the destination operand. The condition codes are set according to the result.\n\nExample usage: orcc %r1, 1, %r1\n\n[Meaning]: Set the least significant bit of %r1 to 1.\n\nObject code: {self.format('10000010100100000110000000000001')}\n\n",
            "orncc": f"\n[Description]: Bitwise NOR the source operands into the destination operand. The con- dition codes are set according to the result.\n\nExample usage: orncc %r1, %r0, %r1\n\n[Meaning]: Complement %r1.\n\nObject code: {self.format('10000010101100000100000000000000')}\n\n",
            "srl": f"\n[Description]: Shift a register to the right by 0 – 31 bits. The vacant bit positions in the left side of the shifted register are filled with 0’s.\n\nExample usage: srl %r1, 3, %r2\n\n[Meaning]: Shift %r1 right by three bits and store in %r2. Zeros are copied into the three most significant bits of %r2.\n\nObject code: {self.format('10000101001100000110000000000011')}\n\n",
            "addcc": f"\n[Description]: Add the source operands into the destination operand using two’s complement arithmetic. The condition codes are set according to the result.\n\nExample usage: addcc %r1, 5, %r1\n\n[Meaning]: Add 5 to %r1.\n\nObject code: {self.format('10000010100000000110000000000101')}\n\n",
            "call": f"\n[Description]: Call a subroutine and store the address of the current instruction (where the call itself is stored) in %r15, which effects a “call and link” operation. In the assem- bled code, the disp30 field in the CALL format will contain a 30-bit displacement from the address of the call instruction. The address of the next instruction to be exe- cuted is computed by adding 4 ´ disp30 (which shifts disp30 to the high 30 bits of the 32-bit address) to the address of the current instruction. Note that disp30 can be negative.\n\nExample usage: call sub_r\n\n[Meaning]: Call a subroutine that begins at location sub_r. For the object code shown below, sub_r is 25 words (100 bytes) farther in memory than the call instruction.\n\nObject code: {self.format('01000000000000000000000000011001')}\n\n",
            "jmpl": f"\n[Description]: Jump and link (return from subroutine). Jump to a new address and store the address of the current instruction (where the jmpl instruction is located) in the destination register.\n\nExample usage: jmpl %r15 + 4, %r0\n\n[Meaning]: Return from subroutine. The value of the PC for the call instruction was previously saved in %r15, and so the return address should be computed for the instruction that follows the call, at %r15 + 4. The current address is discarded in %r0.\n\nObject code: {self.format('10000001110000111110000000000100')}\n\n",
            "be": f"\n[Description]: If the z condition code is 1, then branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the z condition code is 0, then control is transferred to the instruction that follows be.\n\nExample usage: be label\n\n[Meaning]: Branch to label if the z condition code is 1. For the object code shown below, label is five words (20 bytes) farther in memory than the be instruction. Object code: {self.format('00000010100000000000000000000101')}\n\n",
            "bneg": f"\n[Description]: If the n condition code is 1, then branch to the address computed by add- ing 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the n condition code is 0, then control is transferred to the instruction that follows bneg.\n\nExample usage: bneg label\n\n[Meaning]: Branch to label if the n condition code is 1. For the object code shown below, label is five words farther in memory than the bneg instruction.\n\nObject code: {self.format('00001100100000000000000000000101')}\n\n",
            "bcs": f"\n[Description]: If the c condition code is 1, then branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the c condition code is 0, then control is transferred to the instruction that follows bcs.\n\nExample usage: bcs label\n\n[Meaning]: Branch to label if the c condition code is 1. For the object code shown below, label is five words farther in memory than the bcs instruction.\n\nObject code: {self.format('00001010100000000000000000000101')}\n\n",
            "bvs": f"\n[Description]: If the v condition code is 1, then branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the v condition code is 0, then control is transferred to the instruction that follows bvs.\n\nExample usage: bvs label\n\n[Meaning]: Branch to label if the v condition code is 1. For the object code shown below, label is five words farther in memory than the bvs instruction.\n\nObject code: {self.format('00001110100000000000000000000101')}\n\n",
            "ba": f"\n[Description]: Branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction.\n\nExample usage: ba label\n\n[Meaning]: Branch to label regardless of the settings of the condition codes. For the object code shown below, label is five words earlier in memory than the ba instruction.\n\nObject code: {self.format('00010000101111111111111111111011')}",
        }

    async def checklol(self, ctx):
        if self.flag:
            if ctx.author.id not in self.cheaters:
                await ctx.send(
                    "Oh you got caught lacking already?\nOn test day?\nYou thought you could get this shit easy, didn't you?\nClose discord, there are no answers available.\nClose discord, you are not passing.\n"
                    "https://tenor.com/view/caught-in-4k-caught-in4k-chungus-gif-19840038"
                )
                self.cheaters.append(ctx.author.id)
                self.names.append(
                    f"{ctx.author} - {ctx.guild.name} | {ctx.message.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC')}"
                )

                return True
        return False

    @commands.command(aliases=["binTotext"])
    async def binTotxt(self, ctx, *, content: commands.clean_content):
        """``binTotxt [hex code from .bin file]`` Converts .bin hex code into assembly."""
        if await self.checklol(ctx):
            return
        content = content.replace("```\n", "").replace("```", "")
        out = (
            f"```c\nAddress\t\t\t  Memory  Content\n{'-'*49}\n"
            + "\n ".join(
                [
                    (
                        f'{int(j[0], 16)}\t{" ".join([str(bin(int(j[1], 16))).lstrip("0b").zfill(32)[m:m + 4] for m in range(0, 32, 4)])}'
                        if len(j) > 1
                        else ""
                    )
                    for j in [i.split() for i in content.split("\n")]
                ]
            )
            + "```"
        )
        await ctx.send(out)

    def arrange(self, code: str, positions: list):
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

    def get_inst(self, ops):
        get_op = lambda op: ops[1][ops[0].index(op)]
        if "op3" in ops[0]:
            ins = f"[op3 = '{self.codes[get_op('op3')]}']"
        elif "cond" in ops[0]:
            ins = f"[cond = '{self.codes[get_op('cond')]}']"
        else:
            ins = ""

        return ins

    def format(self, content, f=False):
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

            a = self.arrange(content, self.c310[form]).split("\n")
            ops = [a[0].split(), a[1].split()]

            ins = self.get_inst(ops)

            t = f"{i}{(21-len(form + ' Format: '))*' '}{form} Format: "
            text.append(
                f"{' '*(22-len(ins)-6)}{ins}{' '*6}{a[0]}\n{(22-len(t))*' '}{t}{a[1]}"
            )
            i += 1
        s = f'\n{60*"-"}\n'
        if f:
            output = "```java\n" + s.join(text) + "\n```"
        else:
            output = "\n" + s.join(text)

        return output

    @commands.command()
    async def formatbin(self, ctx, *, content: commands.clean_content):
        """``formatbin [binary machine code]`` tries to find format of machine code"""
        if await self.checklol(ctx):
            return
        content = content.replace("```", "")
        output = self.format(content, True)
        await ctx.send(output)

    @commands.command()
    async def spaceout(self, ctx, *, content: commands.clean_content):
        """``spaceout [binary machine code]`` spaces out your binary code"""
        if await self.checklol(ctx):
            return
        c = content.replace(" ", "").replace("```", "")
        x = " ".join([c[i : i + 4] for i in range(0, len(c), 4)])
        await ctx.send(f"```java\n{x}```")

    @commands.command(aliases=["instruct"])
    async def instruction(self, ctx, *, content: commands.clean_content):
        """``instruction [arc instruction]`` get info on an arc command"""
        if await self.checklol(ctx):
            return
        content = content.replace(" ", "").lower()
        if content in self.instructions:
            await ctx.send(
                f"**Instruction:** `{content}` ```ini\n{self.instructions[content]}```"
            )
        else:
            await ctx.send(
                f"`Unkown instruction! Possible instructions are {list(self.instructions.keys())}`"
            )

    def twos_compliment(self, og_binary):
        if og_binary[0] == "1":
            binary = og_binary.replace("0", "$").replace("1", "0").replace("$", "1")
            val = int(binary, 2) + 1
            n = "{0:b}".format(val)
            binary = og_binary[0] * (len(og_binary) - len(n)) + n
        else:
            binary = og_binary
        return binary

    def ones_compliment(self, og_binary):
        if og_binary[0] == "1":
            temp = og_binary[1:]
            binary = og_binary[0] + temp.replace("0", "$").replace("1", "0").replace(
                "$", "1"
            )
        else:
            binary = og_binary

        return binary

    @commands.command()
    async def twoscomp(self, ctx, *, content: commands.clean_content):
        """``twoscomp [binary number]`` resturns the twos compliment representation of a binary number. Requires the sign bit."""
        if await self.checklol(ctx):
            return
        content = content.replace(" ", "")
        await ctx.send("```java\n" + self.twos_compliment(content) + "```")

    @commands.command()
    async def onescomp(self, ctx, *, content: commands.clean_content):
        """``onescomp [binary number]`` resturns the twos compliment representation of a binary number"""
        if await self.checklol(ctx):
            return
        content = content.replace(" ", "")
        await ctx.send("```java\n" + self.ones_compliment(content) + "```")

    def float_to_bin(self, num):
        num1 = bin(int(str(num).split(".")[0])).split("b")

        num2 = float("0" + "." + str(num).split(".")[1])
        sign = ["-", "1"] if num < 0 else ["", "0"]

        b = ""
        for i in range(23):
            num2 *= 2
            b += (
                str(int(str(num2)[0]) // int(str(num2)[0]))
                if str(num2)[0] != "0"
                else "0"
            )
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

        step2 = f"{sign[0]}1.{num1[1][1:]}{b2})2 x2^{exponent}"

        exponent_b = bin(exponent + 127).split("b")[1].zfill(8)

        bin_float = f"{num1[1][1:]}{b2}"
        if len(bin_float) > 23:
            bin_float = bin_float[:23]

        step3 = f"{sign[1]} {exponent_b} {bin_float}{'0'*(23-len(bin_float))}"

        return step1, step2, step3

    def bin_to_float(self, bits):
        bits = bits.replace(" ", "")
        sign = "-" if bits[0] == "1" else ""
        exponent = (int(bits[1:9], 2) - 127) - 23
        mantissa = int("1" + bits[9:], 2)

        ans = mantissa * 2 ** exponent
        ans = float(f"{ans:0.6f}")
        return f"{sign}{ans}"

    @commands.command()
    async def bintofloat(self, ctx, *, content: commands.clean_content):
        """``bintofloat [bin]`` Converts a binary single (+/-) into its decimal representation.(Single) (IEE754)"""
        if await self.checklol(ctx):
            return
        content = content.replace(" ", "")
        await ctx.send(bin_to_float(content))

    @commands.command()
    async def floattobin(self, ctx, *, content: commands.clean_content):
        """``floattobin [float]`` Converts a float (+/-) into its binary representation with steps. (Single) (IEE754)"""
        if await self.checklol(ctx):
            return
        content = float(content.replace(" ", ""))
        step1, step2, step3 = self.float_to_bin(content)
        await ctx.send(
            f"Step 1 - Convert to target base: `{step1}`\nStep 2 - Normalize: `{step2}`\nStep 3 - Fill in bits: `{step3}`\n\n```{' '*(len(str(content))+7)}s exponent   mantissa/fraction  \n{content})10 => {step3}```"
        )

    @commands.command()
    @commands.is_owner()
    async def caught(self, ctx):
        """``owner only``"""
        await ctx.send("```" + "\n".join(self.names) + "```")

    @commands.command()
    @commands.is_owner()
    async def snap(self, ctx):
        """``owner only``"""
        self.flag = True if not self.flag else False
        self.cheaters = []
        await ctx.send("Flag is " + str(self.flag))

    @commands.command()
    async def sethi(self, ctx, *, content: commands.clean_content):
        """``sethi [hex number]`` sets high the first 22 bits and low the last 10"""
        if await self.checklol(ctx):
            return
        if "0x" not in content:
            content = "0x" + content
        content = bin(int(content, 16)).split("b")[1]

        num = (content + ("0" * 10)).zfill(32)
        await ctx.send("```java\n" + num + "```")

    @commands.command()
    async def psr(self, ctx, *, content: commands.clean_content):
        """``psr [psr code]`` tells you what flags have been set."""
        if await self.checklol(ctx):
            return

        c = content.replace(" ", "").replace("```", "")
        x = [c[i : i + 4] for i in range(0, len(c), 4)]

        # nzvc
        msg = ""
        if x[2][0] == "1":
            msg += "**N:** `operation has resulted in a negative number`\n"
        if x[2][1] == "1":
            msg += "**Z:** `operation has resulted to zero`\n"
        if x[2][2] == "1":
            msg += "**V:** `operation has resulted to an overflow`\n"
        if x[2][3] == "1":
            msg += "**C:** `operation has resulted in a requirement to carry`\n"

        await ctx.send(msg)

    @commands.command()
    async def srl(self, ctx, bits, *, content: commands.clean_content):
        """``srl [bits to shift (base 10)] [binary number]`` shifts a binary number down filling in zeros from the left"""
        content = content.replace(" ", "")[: 32 - int(bits)].zfill(32)
        await ctx.send(f"```java\n{content}```")


def setup(bot):
    bot.add_cog(Cps310(bot))
