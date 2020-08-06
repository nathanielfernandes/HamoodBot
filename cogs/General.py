import os
import sys
import random
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import image_functions

#Messaging cog that checks for profantiy and also provide some simple chat commands
class General(commands.Cog):
    """General Commands"""
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
        self.possible_responses = ['hello', 'hi', 'hey', "what's up"]
        self.replies = [
            'what do you want {0.author.mention}?',
            'what {0.author.mention}?',
            'huh?',
            'yeah {0.author.mention}?',
            "what's up"]
        self.bad_replies = ["go away", "stop calling me"]

    @commands.command(aliases=['hello','hi','hey', 'yo'])
    async def greet(self, ctx):
        """greets the user"""
        
        await ctx.send(f"{random.choice(self.possible_responses)} {ctx.author.mention}")

    @commands.command()
    async def hamood(self, ctx):
        """calls hamood"""    
        member = ctx.author
        if self.last_member is None or self.last_member.id != member.id:
            await ctx.send(random.choice(self.replies).format(ctx))
        else:
            await ctx.send(random.choice(self.bad_replies).format(ctx))
        self.last_member = member

    @commands.command()
    async def clap(self, ctx, *content:str):
        """claps ur sentence"""
        msg = ''
        for word in content:
            msg += '**' + word + '**' + ':clap:'
        await ctx.send(msg)

    @commands.command()
    async def repeat(self, ctx, times: int, *, content: commands.clean_content):
        """Repeats a message multiple times."""
        msg = ''
        for i in range(times):
            msg += content + '\n'
        await ctx.send(msg)

    @commands.command()
    async def echo(self, ctx, *, content: commands.clean_content):
        """echos a message."""
        for i in range(random.randint(1,5)):
            await ctx.send(content)

    @commands.command()
    async def no(self, ctx, content:str):
        """no you"""
        if (content == 'u' or content == 'you'):
            #await ctx.channel.purge(limit=1)
            uno = image_functions.unoCard()
            await ctx.send(file=discord.File(uno))

    @commands.command(aliases=["movie time"])
    async def shrek(self, ctx):
        """the entire shrek movie as a 90 min long gif"""
        await ctx.send("https://imgur.com/gallery/IsWDJWa")


def setup(bot):
    bot.add_cog(General(bot))  
