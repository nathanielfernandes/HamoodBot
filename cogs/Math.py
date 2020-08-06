import discord
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['+'])
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(f'**{str(left + right)}**')
            
    @commands.command(aliases=['*'])
    async def multiply(self, ctx, left: int, right: int):
        """multiplies two numbers together."""
        await ctx.send(f'**{str(left * right)}**')

    @commands.command(aliases=['-'])
    async def subtract(self, ctx, left: int, right: int):
        """subtracts two numbers together."""
        await ctx.send(f'**{str(left - right)}**')

    @commands.command(aliases=['/'])
    async def divide(self, ctx, left: int, right: int):
        """divides two numbers together."""
        await ctx.send(f'**{str(left / right)}**')


def setup(bot):
    bot.add_cog(Math(bot))  
