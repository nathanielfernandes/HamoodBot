import os
import sys
import random
import urllib.request
import json
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import zodiac
import message_functions


class Fun(commands.Cog):
    """Random Fun Commands"""
    def __init__(self, bot):
        self.bot = bot
        self.url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
        self.words = json.loads(self.url.read())

    # @commands.command()
    # @commands.has_role("IT")
    # async def tag(self, ctx, member: discord.Member):
    #     """tags a user"""
    #     victim = member
    #     user = ctx.message.author

    #     if str(victim) == 'Hamood#3840':
    #         await ctx.send(f"{ctx.author.mention}, im on time out")
    #     elif (str(victim) == str(user)):
    #         await ctx.send(f"{ctx.author.mention}, you can't tag yourself")
    #     else:
    #         await user.remove_roles(discord.utils.get(user.guild.roles, name='IT'))
    #         await victim.add_roles(discord.utils.get(victim.guild.roles, name='IT'))
    #         await ctx.send((f"{member} is now it!").format(ctx))

    @commands.command()
    async def pp(self, ctx):
        """``pp`` returns your pp size"""
        size = '8'
        length =  ''
        for i in range(random.randint(0,50)):
            length += '='
        size = size + length + 'D'
        await ctx.send(f'{ctx.author.mention} :eggplant: size is **{size}**')

    @commands.command()
    async def sortinghat(self, ctx):
        """``sortinghat`` sorts you to one of the Hogwarts houses"""
        houses = ['Gryffindor', 'Hufflepuff', 'Slytherin', 'Ravenclaw']
        house = random.choice(houses)
        await ctx.send(f'{ctx.author.mention}, you belong to the **{house}** house!')

    @commands.command()
    async def vibecheck(self, ctx):
        """``vibecheck`` vibechecks you"""
        random_word = random.choice(self.words)
        await ctx.send(f"{ctx.author.mention} your vibe checked out to be **{random_word}**")
        await ctx.message.add_reaction('✔️')

    @commands.command()
    async def vibe(self, ctx):
        """``vibe`` vibechecks you but better"""
        fonts = self.bot.get_cog('Fonts')
        random_word = random.choice(self.words)
        await ctx.send(f'{ctx.author.mention} your vibe checked out to be:')
        await fonts.textPrep(ctx, (random_word), 'random', 500, 'random', 100)


    @commands.command(aliases=['roast me', 'roastme'])
    async def roast(self, ctx):
        """``roast`` roasts/insults you"""
        roast = message_functions.getRoast()
        await ctx.send(f'{ctx.author.mention} {roast}')

    @commands.command(aliases=["pop", "bubble"])
    async def bubblewrap(self, ctx, w=3, h=3):
        """``bubblewrap [height] [width]`` makes bubblewrap"""
        if w > 12:
            w = 12
        if h > 12:
            h = 12
        wrap = ''
        w = "||pop||"*int(w)
        for i in range(h):
            wrap += w + "\n"
        await ctx.send(wrap)

    @commands.command(aliases=['sign'])
    async def zodiac(self, ctx, month1: str, day1: int, month2:str, day2: int, quick="slow"):
        """``zodiac [mmm] [dd] [mmm] [dd]`` lets you test your zodiac's compatibilty with another"""
        sign1 = zodiac.getZodiac(month1, day1)
        sign2 = zodiac.getZodiac(month2, day2)

        compatibility = zodiac.getCompatibility(sign1, sign2)

        if (quick == "slow"):
            await ctx.send(f"person 1 is a **{sign1}**, person 2 is a **{sign2}**, and they are about **{compatibility}** compatible")
        else:
            await ctx.send(f'**{sign1}** and **{sign2}** are about **{compatibility}** compatible')

    @commands.command()
    async def match(self, ctx, *, content: commands.clean_content):
        """``match [person1] [person2]`` randomly gives a match percentage between two people"""
        match = str(random.randint(0,100))
        content = content.split(', ')
        left, right = content
        await ctx.send(f'**{left}** and **{right}** are **{match}%** compatible')


def setup(bot):
    bot.add_cog(Fun(bot))  