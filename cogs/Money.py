import discord
from discord.ext import commands

import modules.checks as checks


class Money(commands.Cog):
    """Commands that reach into ur pockets"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Money(bot))
