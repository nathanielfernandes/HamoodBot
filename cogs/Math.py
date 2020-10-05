import os
import discord
from discord.ext import commands

from modules.math_functions import (
    base_conversion,
    solve_eq,
    run_code,
    calc_eq,
    graph_eq,
)


class Math(commands.Cog):
    """Quick Mafs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def base(self, ctx, *, content: commands.clean_content):
        """``base [number)base], [next base]`` converts numbers between bases"""
        try:
            number, base2 = content.split(", ")
            number, base1 = number.split(")")
        except ValueError:
            await ctx.send("Invalid Input!")
            return

        answer = base_conversion(number, base1, base2)
        await ctx.send(f"**Base {base1}:** `{number}`\n**Base {base2}:** `{answer}`\n")

    @commands.command()
    async def calc(self, ctx, *, content: commands.clean_content):
        """``calc [equation]`` calculates the answer to the given equation"""
        await ctx.send(f"`{calc_eq(content)}`")

    @commands.command()
    @commands.cooldown(4, 10, commands.BucketType.user)
    async def solve(self, ctx, *, content: commands.clean_content):
        """``solve [equation]`` solves for variables in most math equations"""
        await ctx.send(f"`{solve_eq(content)}`")

    @commands.command()
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def graph(self, ctx, *, content: commands.clean_content):
        """``graph [equation], [next equation]`` graphs given equation"""
        content = content.split(", ") if ", " in content else [content]
        for i in range(len(content)):
            if ": " in content[i]:
                content[i] = content[i].split(": ")
            elif ": " not in content[i]:
                content[i] = [content[i]]

        done, graph = graph_eq(content, f"{ctx.author}'s Graph")
        if done:
            await ctx.send(file=discord.File(graph))
            os.remove(graph)
        else:
            await ctx.send("`Could not graph equation`")

    @commands.command()
    @commands.is_owner()
    async def py(self, ctx, *, content: commands.clean_content):
        """``py [code]`` runs python code and outputs to the chat (owner command)"""
        out = run_code(content.strip("`"))
        await ctx.send(f"```py\n{out}```")


def setup(bot):
    bot.add_cog(Math(bot))

