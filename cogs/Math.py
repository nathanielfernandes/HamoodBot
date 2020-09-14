import discord
from discord.ext import commands

from modules.math_functions import base_conversion, solve_eq, run_code, calc_eq


class Math(commands.Cog):
    """Quick Mafs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def base(self, ctx, *, content: commands.clean_content):
        """``base [number)base] [base]`` converts numbers between bases"""
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
    async def solve(self, ctx, *, content: commands.clean_content):
        """``solve [equation]`` solves for variables in simple math equations"""
        await ctx.send(f"`{solve_eq(content)}`")

    @commands.command()
    @commands.is_owner()
    async def py(self, ctx, *, content: commands.clean_content):
        """``py [code]`` lets me run code and out put it to the chat"""
        out = run_code(content.strip("`"))
        await ctx.send(f"```py\n{out}```")


def setup(bot):
    bot.add_cog(Math(bot))

