import discord
from discord.ext import commands

from modules.chem_functions import ChemEq


class Chemistry(commands.Cog):
    """Quick Chem"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(4, 10, commands.BucketType.user)
    async def balance(self, ctx, *, content: commands.clean_content):
        """``balance [equation] ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`` balances chemical equations"""
        answer = ChemEq(content).balance()
        await ctx.send(f"**Balanced Equation:** {answer}")


def setup(bot):
    bot.add_cog(Chemistry(bot))
