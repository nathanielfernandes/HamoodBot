import discord
from discord.ext import commands


class Dev(commands.Cog):
    """Dev Commands"""

    def __init__(self, bot):
        self.bot = bot
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

        self.instructions = {
            "ld": "\n[Description]: Load a register from main memory. The memory address must be aligned on a word boundary (that is, the address must be evenly divisible by 4). The address is computed by adding the contents of the register in the rs1 field to either the contents of the register in the rs2 field or the value in the simm13 field, as appropriate for the con- text.\n\n",
            "st": "\n[Description]: Store a register into main memory. The memory address must be aligned on a word boundary. The address is computed by adding the contents of the register in the rs1 field to either the contents of the register in the rs2 field or the value in the simm13 field, as appropriate for the context. The rd field of this instruction is actually used for the source register.\n\n",
            "sethi": "\n[Description]: Set the high 22 bits and zero the low 10 bits of a register. If the operand is 0 and the register is %r0, then the instruction behaves as a no-op (NOP), which means that no operation takes place.\n\nExample usage: sethi 0x304F15, %r1\n\n[Meaning]: Set the high 22 bits of %r1 to (304F15)16, and set the low 10 bits to zero.\n\nObject code: 00000011001100000100111100010101\n\n",
            "andcc": "\n[Description]: Bitwise AND the source operands into the destination operand. The condition codes are set according to the result.\n\nExample usage: andcc %r1, %r2, %r3\n\n[Meaning]: Logically AND %r1 and %r2 and place the result in %r3.\n\nObject code: 10000110100010000100000000000010\n\n",
            "orcc": "\n[Description]: Bitwise OR the source operands into the destination operand. The condition codes are set according to the result.\n\nExample usage: orcc %r1, 1, %r1\n\n[Meaning]: Set the least significant bit of %r1 to 1.\n\nObject code: 10000010100100000110000000000001\n\n",
            "orncc": "\n[Description]: Bitwise NOR the source operands into the destination operand. The con- dition codes are set according to the result.\n\nExample usage: orncc %r1, %r0, %r1\n\n[Meaning]: Complement %r1.\n\nObject code: 10000010101100000100000000000000\n\n",
            "srl": "\n[Description]: Shift a register to the right by 0 – 31 bits. The vacant bit positions in the left side of the shifted register are filled with 0’s.\n\nExample usage: srl %r1, 3, %r2\n\n[Meaning]: Shift %r1 right by three bits and store in %r2. Zeros are copied into the three most significant bits of %r2.\n\nObject code: 10000101001100000110000000000011\n\n",
            "addcc": "\n[Description]: Add the source operands into the destination operand using two’s complement arithmetic. The condition codes are set according to the result.\n\nExample usage: addcc %r1, 5, %r1\n\n[Meaning]: Add 5 to %r1.\n\nObject code: 10000010100000000110000000000101\n\n",
            "call": "\n[Description]: Call a subroutine and store the address of the current instruction (where the call itself is stored) in %r15, which effects a “call and link” operation. In the assem- bled code, the disp30 field in the CALL format will contain a 30-bit displacement from the address of the call instruction. The address of the next instruction to be exe- cuted is computed by adding 4 ´ disp30 (which shifts disp30 to the high 30 bits of the 32-bit address) to the address of the current instruction. Note that disp30 can be negative.\n\nExample usage: call sub_r\n\n[Meaning]: Call a subroutine that begins at location sub_r. For the object code shown below, sub_r is 25 words (100 bytes) farther in memory than the call instruction. Object code: 01000000000000000000000000011001\n\n",
            "jmpl": "\n[Description]: Jump and link (return from subroutine). Jump to a new address and store the address of the current instruction (where the jmpl instruction is located) in the destination register.\n\nExample usage: jmpl %r15 + 4, %r0\n\n[Meaning]: Return from subroutine. The value of the PC for the call instruction was previously saved in %r15, and so the return address should be computed for the instruction that follows the call, at %r15 + 4. The current address is discarded in %r0.\n\nObject code: 10000001110000111110000000000100\n\n",
            "be": "\n[Description]: If the z condition code is 1, then branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the z condition code is 0, then control is transferred to the instruction that follows be.\n\nExample usage: be label\n\n[Meaning]: Branch to label if the z condition code is 1. For the object code shown below, label is five words (20 bytes) farther in memory than the be instruction. Object code: 00000010100000000000000000000101\n\n",
            "bneg": "\n[Description]: If the n condition code is 1, then branch to the address computed by add- ing 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the n condition code is 0, then control is transferred to the instruction that follows bneg.\n\nExample usage: bneg label\n\n[Meaning]: Branch to label if the n condition code is 1. For the object code shown below, label is five words farther in memory than the bneg instruction.\n\nObject code: 00001100100000000000000000000101\n\n",
            "bcs": "\n[Description]: If the c condition code is 1, then branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the c condition code is 0, then control is transferred to the instruction that follows bcs.\n\nExample usage: bcs label\n\n[Meaning]: Branch to label if the c condition code is 1. For the object code shown below, label is five words farther in memory than the bcs instruction.\n\nObject code: 00001010100000000000000000000101\n\n",
            "bvs": "\n[Description]: If the v condition code is 1, then branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction. If the v condition code is 0, then control is transferred to the instruction that follows bvs.\n\nExample usage: bvs label\n\n[Meaning]: Branch to label if the v condition code is 1. For the object code shown below, label is five words farther in memory than the bvs instruction.\n\nObject code: 00001110100000000000000000000101\n\n",
            "ba": "\n[Description]: Branch to the address computed by adding 4 ´ disp22 in the Branch instruction format to the address of the current instruction.\n\nExample usage: ba label\n\n[Meaning]: Branch to label regardless of the settings of the condition codes. For the object code shown below, label is five words earlier in memory than the ba instruction.\n\nObject code: 00010000101111111111111111111011",
        }

    def to_id(self, name):
        return name.replace(" ", "_").lower()

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        """``logout`` logs hamood out"""
        await ctx.send("**goodbye**")
        await self.bot.aioSession.close()
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, aType: str, uRL: str, *, aName: commands.clean_content):
        """``status [type] [url] [activity]`` lets me change hamoods status"""
        if aType == "playing":
            await self.bot.change_presence(activity=discord.Game(name=aName))
        elif aType == "listening":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, name=aName
                )
            )
        elif aType == "watching":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=aName
                )
            )
        elif aType == "streaming":
            await self.bot.change_presence(
                activity=discord.Streaming(name=aName, url=uRL)
            )

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """``reload [cog name]`` reloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got reloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """``unload [cog name]`` unloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got unloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be unloaded:`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        """``load [cog name]`` loads the requested cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got loaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded:`")
            raise

    @commands.command()
    @commands.is_owner()
    async def get_item(self, ctx, item_id, amount=1):
        """``get_item [item_id] [amount]`` get any item"""
        amount = int(amount)
        await self.bot.inventories.add_inventory(ctx.guild.id)
        await self.bot.inventories.add_member(ctx.guild.id, ctx.author.id)
        await self.bot.inventories.add_item(
            ctx.guild.id, ctx.author.id, self.to_id(item_id), int(amount)
        )
        await ctx.send(f"`You recieved {item_id} x{amount}`")

    @commands.command()
    @commands.is_owner()
    async def print_money(self, ctx, amount):
        """``print_money [amount]`` get any amount of money"""
        await self.bot.currency.add_server(ctx.guild.id)
        await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)
        await self.bot.currency.update_wallet(ctx.guild.id, ctx.author.id, int(amount))

        await ctx.send(f"`You recieved ⌬ {int(amount):,}`")

    @commands.command()
    @commands.is_owner()
    async def wipe(self, ctx, member: discord.Member = None):
        if member is not None:
            # await self.bot.leaderboards.delete_member(member.guild.id, member.id)
            await self.bot.currency.delete_member(member.guild.id, member.id)
            await self.bot.inventories.delete_member(member.guild.id, member.id)

            await ctx.send(f"{member.mention} has been wiped from the db")

    @commands.command()
    @commands.is_owner()
    async def timeout(self, ctx, member: discord.Member = None):
        if member is not None:
            if member.id in self.bot.timeout_list:
                self.bot.timeout_list.remove(member.id)
                await ctx.send(f"**{member}** has been taken out of time out.")
            else:
                self.bot.timeout_list.append(member.id)
                await ctx.send(f"**{member}** has been put in time out.")

    @commands.command()
    @commands.is_owner()
    async def timeout_corner(self, ctx):
        corner = "\n".join(
            [str(self.bot.get_user(id_)) for id_ in self.bot.timeout_list]
        )
        await ctx.send(f"```{corner}```")

    @commands.command(aliases=["binTotext"])
    async def binTotxt(self, ctx, *, content: commands.clean_content):
        """``binTotxt [hex code from .bin file]`` Converts .bin hex code into assembly."""
        content = content.replace("```\n", "").replace("```", "")
        out = (
            f"```c\nAddress\t\t\t  Memory  Content\n{'-'*49}"
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

    def format(self, content):
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
            t = f"{i}{(21-len(form + ' Format: '))*' '}{form} Format: "
            text.append(f"{' '*22}{a[0]}\n{(22-len(t))*' '}{t}{a[1]}")
            i += 1
        s = f'\n{60*"-"}\n'
        output = "```java\n" + s.join(text) + "\n```"
        return output

    @commands.command()
    async def formatbin(self, ctx, *, content: commands.clean_content):
        """``formatbin [binary machine code]`` tries to find format of machine code"""
        content = content.replace(" ", "").replace("```", "")
        output = self.format(content)
        await ctx.send(output)

    @commands.command(aliases=["instruct"])
    async def instruction(self, ctx, *, content: commands.clean_content):
        """``instruction [arc instruction]`` get info on an arc command"""
        content = content.replace(" ", "").lower()
        if content in self.instructions:
            await ctx.send(
                f"**Instruction:** `{content}` ```ini\n{self.instructions[content]}```"
            )
        else:
            await ctx.send(
                f"`Unkown instruction! Possible instructions are {list(self.instructions.keys())}`"
            )


def setup(bot):
    bot.add_cog(Dev(bot))
