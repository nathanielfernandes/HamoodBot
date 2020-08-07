import discord
from discord.ext import commands

class Math(commands.Cog):
    """Quick Mafs"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['+'])
    async def add(self, ctx, left: int, right: int):
        """``add [number1] [number2]`` adds two numbers together"""
        await ctx.send(f'**{str(left + right)}**')
            
    @commands.command(aliases=['*'])
    async def multiply(self, ctx, left: int, right: int):
        """``multiply [number1] [number2]`` multiplies two numbers together"""
        await ctx.send(f'**{str(left * right)}**')

    @commands.command(aliases=['-'])
    async def subtract(self, ctx, left: int, right: int):
        """``subtract [number1] [number2]`` subtracts two numbers together"""
        await ctx.send(f'**{str(left - right)}**')

    @commands.command(aliases=['/'])
    async def divide(self, ctx, left: int, right: int):
        """``divide [number1] [number2]`` divides two numbers together"""
        await ctx.send(f'**{str(left / right)}**')


def setup(bot):
    bot.add_cog(Math(bot))  
