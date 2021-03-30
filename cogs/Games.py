import os
import discord
from discord.ext import commands

from modules.games.ConnectFour import ConnectFour
import modules.checks as checks


class Games(commands.Cog):
    """Play Games!"""  # all games auto delete if theres no input for 2 minutes

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            _id = str(payload.guild_id) + str(payload.user_id)
            if _id in self.bot.games:
                await self.bot.games[_id].on_reaction(payload)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def connect4t(self, ctx, member: discord.Member = None, wager=0):
        """``connect [@opponent] [wager]`` starts a new connect 4 game"""
        wager = int(wager)
        game = ConnectFour(playerTwo=member, ctx=ctx, bot=self.bot, wager=wager)
        await game.setup_game()

    @commands.command()
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def leave(self, ctx):
        """``leave`` leaves any game you are currently in."""
        _id = str(ctx.guild_id) + str(ctx.author.id)
        if _id not in self.bot.games:
            return await ctx.send("You are not currently in a game!")

        await self.bot.games[_id].delete_game(member=ctx.author)
        await ctx.send(f"{ctx.author.mention}, you have left your game!")


def setup(bot):
    bot.add_cog(Games(bot))
