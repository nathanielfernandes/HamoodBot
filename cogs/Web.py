import os
import discord
from discord.ext import commands

from modules.web_scraping import covid_info  # , insta_profile
from modules.image_search import ImgSearch

import json

blacklist = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/blacklist.json"
    )
)["commandblacklist"][f"{os.path.basename(__file__)[:-3]}"]


def isAllowedCommand():
    async def predicate(ctx):
        return ctx.guild.id not in blacklist

    return commands.check(predicate)


class Web(commands.Cog):
    """Information Scraped From The Web"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
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

    # @commands.command(aliases=["instagram"])
    # @commands.has_permissions(embed_links=True)
    # async def insta(self, ctx, username=None):
    #     """``insta [username]`` gets an instagram profile"""
    #     async with ctx.typing():
    #         exists, profile = insta_profile(username)
    #         if exists:
    #             line2 = f"**Post:** {profile['posts']}   **Followers:** {profile['followers']}  **Following:** {profile['following']}"
    #             name = profile["name"] if profile["name"] != "" else "`no name`"
    #             bio = profile["bio"] if profile["bio"] != "" else "`no bio`"
    #             link = f"{profile['link']}\n" if profile["link"] != None else ""

    #             line1 = f"**{name}**\n{bio}\n{link}"

    #             embed = discord.Embed(
    #                 title=username,
    #                 url=profile["url"],
    #                 colour=14104244,
    #                 description=f"{line1}\n{line2}",
    #                 timestamp=ctx.message.created_at,
    #             )
    #             embed.set_author(
    #                 name="Instagram",
    #                 icon_url="https://cdn.discordapp.com/attachments/741384050387714162/757034757971378176/600px-Instagram_logo_2016.png",
    #             )
    #             embed.set_thumbnail(url=profile["pfp"])
    #             embed.set_footer(text=f"Requested by {ctx.author}",)

    #             await ctx.send(embed=embed)
    #         else:
    #             await ctx.send("`Profile Not Found`")

    @commands.command()
    @commands.is_owner()
    async def google(self, ctx, *, query: commands.clean_content):
        """``google [image]`` googles an image (owner command)"""
        image = ImgSearch(query)
        await ctx.send(f"This is the first result for **'{query}'**:")
        await ctx.send(file=discord.File(image))
        os.remove(image)


def setup(bot):
    bot.add_cog(Web(bot))

