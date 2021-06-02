import os
import discord
from discord.ext import commands

from modules.math_functions import *
import modules.checks as checks


class Math(commands.Cog):
    """Quick Mafs"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.command()
    @checks.isAllowedCommand()
    async def base(self, ctx, *, content: commands.clean_content):
        """``base [number)base], [next base]`` converts numbers between bases"""
        try:
            number, base2 = content.split(", ")
            number, base1 = number.split(")")
        except ValueError:
            await ctx.send("Invalid Input!")
            return
        answer = await base_conversion(number, int(base1), int(base2))
        embed = discord.Embed(
            title=f"Base {base1} to Base {base2}:",
            description=f"**Base {base1}:** `{number}`\n**Base {base2}:** `{answer}`\n",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    # await ctx.send(f"**Base {base1}:** `{number}`\n**Base {base2}:** `{answer}`\n")

    @commands.command(aliases=["calculate"])
    @checks.isAllowedCommand()
    async def calc(self, ctx, *, content: commands.clean_content):
        """``calc [equation]`` calculates the answer to the given equation (assumes natural log unless specified [log(base, number)]"""
        content = "".join([x for x in content])

        out = str(await calc_eq(content))
        if len(out) > 2000:
            out = out[:1950] + " Exceded Character Limit! "

        embed = discord.Embed(
            title="Calculate:",
            description=f"{content} **=**\n```{out}```",
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)

    #  await ctx.send(f"**Answer: **`{out}`")

    @commands.command(aliases=["aliases"])
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.user)
    async def derivative(self, ctx, number, *, content: commands.clean_content):
        """``derivative [nth derivative] [equation]`` solves for the nth dervative of an equation"""
        ext = ["th", "st", "nd", "rd"]
        number = int(number)
        answer = await get_derivative(content, number)
        embed = discord.Embed(
            title=f"{number}{ext[number] if number <= 3 else 'th'} Derivative of :",
            description=f"{content} **=**\n```{answer}```",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.user)
    async def solve(self, ctx, *, content: commands.clean_content):
        """``solve [equation]`` solves for variables in most math equations"""
        embed = discord.Embed(
            title="Solve:",
            description=f"**{content}**:\n```{await solve_eq(content)}```",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    #     await ctx.send(f"`{solve_eq(content)}`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 10, commands.BucketType.channel)
    async def graph(self, ctx, *, content: commands.clean_content):
        """``graph [equation], [next equation]`` graphs given equation"""
        content = content.split(", ") if ", " in content else [content]
        for i in range(len(content)):
            if ": " in content[i]:
                content[i] = content[i].split(": ")
            elif ": " not in content[i]:
                content[i] = [content[i]]

        done, graph = await graph_eq(content, f"{ctx.author}'s Graph")
        if done:
            await ctx.send(file=discord.File(graph))
            os.remove(graph)
        else:
            await ctx.send("`Could not graph equation`")

    @commands.command(aliases=["ltx", "fool"])
    @checks.isAllowedCommand()
    @commands.cooldown(2, 10, commands.BucketType.channel)
    async def latex(self, ctx, *, content: commands.clean_content):
        """``latex [latex formula]`` converts latex to regular text"""

        text, e = await latex_to_text(content)
        if e is None:
            try:
                await ctx.send(file=discord.File(text))
            except Exception:
                await ctx.send("`Could Not Convert Formula`")

            os.remove(text)
        else:
            await ctx.send(f"```{e}```")


def setup(bot):
    bot.add_cog(Math(bot))

