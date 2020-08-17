import os
import sys
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import message_functions

class Events(commands.Cog): 
    """Handles Any Discord Events"""
    def __init__(self, bot):
        self.bot = bot

        file = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/textFiles/errors.txt'
        self.error_solutions = message_functions.convert_to_dict(file)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have the permission to do that")
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                await ctx.send(self.error_solutions[str(ctx.command)])
            except Exception:
                print('error')
                raise error


def setup(bot):
    bot.add_cog(Events(bot))  

