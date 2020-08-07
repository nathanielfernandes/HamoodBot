import random
import discord
from discord.ext import commands

class Chance(commands.Cog):
    """Take a Chance"""
    def __init__(self, bot):
        self.bot = bot
        self.possible_responses = [
            "hell naw",
            "i highley doubt it",
            "how am i supposed to know",
            "i guess its possible",
            "fo sho",
            "maybe",
            "stop asking",
            "yeah",
            "nah",
            "i dont care",
            "ofcourse",
            "not really"
            ]

    @commands.command(aliases= ['8ball','does','would','should','could','can','do','will','is','am i'])
    async def eightball(self, ctx):
        """``eightball`` Hamood shakes his magic 8ball"""
        await ctx.send(f"{random.choice(self.possible_responses)}, {ctx.author.mention}")

    @commands.command(aliases=['coin'])
    async def flip(self, ctx): 
        """``flip`` flips a coin"""
        possible_responses = ['heads', 'tails']
        await ctx.send(f'**{random.choice(possible_responses)}**, {ctx.author.mention}')

    @commands.command(aliases=['dice'])
    async def roll(self, ctx, dice: str):
        """``roll [NdN]`` Rolls a dice in NdN format."""
        rolls, limit = map(int, dice.split('d'))
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *, content: commands.clean_content):
        """``choose [choice1], [choice2], [choice3]`` Chooses between multiple choices."""
        content = content.split(', ')
        await ctx.send(random.choice(content))


def setup(bot):
    bot.add_cog(Chance(bot))  