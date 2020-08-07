import os
import sys
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import web_scraping
import image_search

class Web(commands.Cog):
    """Information Scraped From The Web"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def covid(self, ctx, country=None):
        """``covid [country]`` gets the latest covid 19 statistics"""

        url, info = web_scraping.covid_info(country)
        msg = ''
        for i, j in info.items():
            msg += i + ' : **' + j + '**' + '\n'
        
        member = ctx.author
        
        if country == None:
            embed = discord.Embed(title="Covid-19 Statistics:", description=msg, colour=member.color, timestamp=ctx.message.created_at, url=url)
        else:
            embed = discord.Embed(title=f"{country}'s Covid-19 Statistics:", description=msg, colour=member.color, timestamp=ctx.message.created_at, url=url)
        await ctx.send(embed=embed)


    @commands.command()
    async def google(self, ctx, *, query: commands.clean_content):
        """``google [image]`` googles an image"""
        image = image_search.ImgSearch(query)
        await ctx.send(f"This is the first result for **'{query}'**:")
        await ctx.send(file=discord.File(image))
        os.remove(image)


def setup(bot):
    bot.add_cog(Web(bot))  