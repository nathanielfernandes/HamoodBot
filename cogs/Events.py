import os
import discord
from discord.ext import commands


class Events(commands.Cog):
    """Handles Any Discord Events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome {member.mention}!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("`You don't have the permission to do that`")
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                s = ctx.command.help
                start = s.find("``") + 2
                end = s.find("``", start)
                await ctx.send(f"```{s[start:end]}```")
            except Exception:
                print("error")
                # raise error


def setup(bot):
    bot.add_cog(Events(bot))

