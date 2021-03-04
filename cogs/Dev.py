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


def setup(bot):
    bot.add_cog(Dev(bot))
