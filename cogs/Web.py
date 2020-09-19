import os
import discord
from discord.ext import commands

from modules.web_scraping import covid_info
from modules.image_search import ImgSearch


class Web(commands.Cog):
    """Information Scraped From The Web"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def covid(self, ctx, country=None):
        """``covid [country]`` gets the latest covid 19 statistics"""

        url, info = covid_info(country)
        msg = ""
        for i, j in info.items():
            msg += i + " : **" + j + "**" + "\n"

        member = ctx.author

        if country == None:
            embed = discord.Embed(
                title="Statistics:",
                description=msg,
                colour=member.color,
                timestamp=ctx.message.created_at,
                url=url,
            )
            embed.set_author(
                name="Covid-19",
                icon_url="https://cdn.discordapp.com/attachments/741384050387714162/756642082172436500/Coronavirus-CDC-645x645.jpg",
            )
        else:
            embed = discord.Embed(
                title=f"{country}'s Statistics:",
                description=msg,
                colour=member.color,
                timestamp=ctx.message.created_at,
                url=url,
            )
            embed.set_author(
                name="Covid-19",
                icon_url="https://cdn.discordapp.com/attachments/741384050387714162/756642082172436500/Coronavirus-CDC-645x645.jpg",
            )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def google(self, ctx, *, query: commands.clean_content):
        """``google [image]`` googles an image"""
        image = ImgSearch(query)
        await ctx.send(f"This is the first result for **'{query}'**:")
        await ctx.send(file=discord.File(image))
        os.remove(image)


def setup(bot):
    bot.add_cog(Web(bot))

