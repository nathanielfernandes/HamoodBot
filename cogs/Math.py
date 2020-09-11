import discord
from discord.ext import commands


class Math(commands.Cog):
    """Quick Mafs"""

    def __init__(self, bot):
        self.bot = bot
        self.chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @commands.command(aliases=["+"])
    async def add(self, ctx, left: int, right: int):
        """``add [number1] [number2]`` adds two numbers together"""
        await ctx.send(f"**{str(left + right)}**")

    @commands.command(aliases=["*"])
    async def multiply(self, ctx, left: int, right: int):
        """``multiply [number1] [number2]`` multiplies two numbers together"""
        await ctx.send(f"**{str(left * right)}**")

    @commands.command(aliases=["-"])
    async def subtract(self, ctx, left: int, right: int):
        """``subtract [number1] [number2]`` subtracts two numbers together"""
        await ctx.send(f"**{str(left - right)}**")

    @commands.command(aliases=["/"])
    async def divide(self, ctx, left: int, right: int):
        """``divide [number1] [number2]`` divides two numbers together"""
        await ctx.send(f"**{str(left / right)}**")

    @commands.command()
    async def base(self, ctx, *, content: commands.clean_content):
        """``base [number)base] [base]`` converts numbers between bases"""
        number, base2 = content.split(", ")
        number, base1 = number.split(")")

        try:
            number, base1, base2 = str(number).upper(), int(base1), int(base2)
            if not 1 < base1 < 37 and not 1 < base2 < 37:
                return
        except ValueError:
            return

        for num in number:
            if num not in self.chars[:base1]:
                return

        temp_number = 0
        for i in range(len(number)):
            temp_number += self.chars.index(number[::-1][i]) * base1 ** i

        answer = ""
        while temp_number >= 1:
            answer = self.chars[temp_number % base2] + answer
            temp_number = temp_number // base2

        content = answer
        await ctx.send(f"**Base {base1}:** `{number}`\n**Base {base2}:** `{content}`\n")


def setup(bot):
    bot.add_cog(Math(bot))

