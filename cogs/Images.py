import os
import discord
from discord.ext import commands

from modules.image_functions import Edit
from modules.web_scraping import scrape


class Images(commands.Cog):
    """Image & Gif Manipulation"""

    def __init__(self, bot):
        self.bot = bot
        self.path = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        self.edit = Edit(None, f"{self.path}/tempImages")

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def deepfry(self, ctx):
        """``deepfry [looks for previous sent images]`` deepfries any image, tasty!"""
        message = await ctx.message.channel.history(limit=40).find(
            lambda m: "https" in str(m.content)
            and (
                ".jpg" in str(m.content)
                or ".png" in str(m.content)
                or ".jpeg" in str(m.content)
                or ".gif" in str(m.content)
            )
        )
        exts = ["jpg", "png", "jpeg", "gif"]

        for e in exts:
            if e in message.content:
                end = e

        name = f"{self.edit.randomNumber()}.{end}"
        save = f"{self.path}/tempImages/{name}"

        new = f"{self.edit.randomNumber()}.{end}"

        scrape(message.content, save)

        deepfried = self.edit.deep_fry(name, new, end)

        await ctx.send(file=discord.File(deepfried))

        os.remove(deepfried)
        os.remove(save)

    # @commands.command()
    # # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.has_permissions(attach_files=True)
    # async def rgb(self, ctx, image=None):
    #     message = await ctx.message.channel.history(limit=20).find(
    #         lambda m: ".gif" in m.content
    #     )

    #     name = f"{self.edit.randomNumber()}.gif"
    #     save = f"{self.path}/tempImages/{name}"

    #     new = f"{self.edit.randomNumber()}.gif"

    #     scrape(message.content, save)

    #     rgbb = self.edit.gif_rgb(name, new)

    #     await ctx.send(file=discord.File(rgbb))

    #     os.remove(rgbb)
    #     os.remove(save)


def setup(bot):
    bot.add_cog(Images(bot))
