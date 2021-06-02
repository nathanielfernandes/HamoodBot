import os
import discord
import textwrap
import random
import json
from io import BytesIO
from discord.ext import commands

from modules.image_functions import makeText
import modules.checks as checks


class Fonts(commands.Cog):
    """Send Messages With Cool Fonts"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.fontDict = json.load(open(f"{self.Hamood.filepath}/data/fonts.json"))
        self.colourDict = json.load(open(f"{self.Hamood.filepath}/data/colours.json"))
        self.save_location = f"{self.Hamood.filepath}/temp"
        self.fonts = f"{self.Hamood.filepath}/fonts"

    async def text_prep(self, ctx, text, font, font_size, colour, wrap=100, send=True):
        if text == ():
            return

        if font == "random":
            font = random.choice(list(self.fontDict.values()))
        elif font in self.fontDict:
            font = self.fontDict[font]

        font = f"{self.fonts}/{font}"

        if colour == "random":
            colour = tuple(random.choice(list(self.colourDict.values())))
        elif colour not in self.colourDict:
            colour = (255, 255, 255, 255)
        else:
            colour = tuple(self.colourDict[colour])

        text = [text]
        for i in range(len(text)):
            text[i] = textwrap.wrap(text[i], width=wrap)
            for a in range(1, len(text[i])):
                text[i][a] = "\n" + text[i][a]
            text[i] = " ".join(text[i])
        text = text[0]

        name = (
            self.save_location
            + "/"
            + "".join(random.choice("123456789") for i in range(12))
            + ".png"
        )

        textImg = makeText(text, font, font_size, colour, name)

        if send:
            await ctx.message.delete()
            await self.Hamood.quick_embed(
                ctx=ctx,
                image=textImg,
                footer={"text": f"Requested by {ctx.author}"},
                color=discord.Color.from_rgb(colour[0], colour[1], colour[2]),
            )
            # embed = self.Hamood.quick_embed(
            #     member=ctx.author, rainbow=True, requested=True, color=colour
            # )
            # self.bot.S3.schedule_upload_bytes(
            #     file_bytes=bio, ext="png", channel_id=ctx.channel.id, embed=embed,
            # )
        else:
            return textImg, colour

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def arial(self, ctx, *, content: commands.clean_content):
        """``arial [msg]`` send a message in a arial font"""
        await self.text_prep(
            ctx, content[:45], "arial", 500, "black",
        )

    @commands.command(aliases=["craft"])
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def minec(self, ctx, *, content: commands.clean_content):
        """``minec [msg]`` send a message in a minecraft font"""
        await self.text_prep(
            ctx, content[:45], "minecraft", 500, "yellow2",
        )

    @commands.command(aliases=["tale"])
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def undertale(self, ctx, *, content: commands.clean_content):
        """``undertale [msg]`` send a message in a undertale font"""
        await self.text_prep(
            ctx, content[:45], "undertale", 500, "white",
        )

    @commands.command(aliases=["rick"])
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def morty(self, ctx, *, content: commands.clean_content):
        """``morty [msg]`` send a message in a morty font"""
        await self.text_prep(
            ctx, content[:45], "get_schwhifty.ttf", 500, "green1",
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gta(self, ctx, *, content: commands.clean_content):
        """``gta [msg]`` send a message in a gta font"""
        await self.text_prep(
            ctx, content[:45], "gta", 500, "white",
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enchant(self, ctx, *, content: commands.clean_content):
        """``enchant [msg]`` send a message in a enchant font"""
        await self.text_prep(
            ctx, content[:45], "minecraft-enchantment.ttf", 500, "white",
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unknown(self, ctx, *, content: commands.clean_content):
        """``unknown [msg]`` send a message in a unknown font"""
        await self.text_prep(ctx, content[:45], "unown.ttf", 500, "black", 100)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pokefont(self, ctx, *, content: commands.clean_content):
        """``pokefont [msg]`` send a message in a pokemon font"""
        await self.text_prep(ctx, content[:45], "pokemon", 500, "steelblue2", 100)

    @commands.command(aliases=["sonic"])
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sega(self, ctx, *, content: commands.clean_content):
        """``sega [msg]`` send a message in a sega font"""
        await self.text_prep(ctx, content[:45], "sega", 500, "navy", 100)

    @commands.command(aliases=["sponge"])
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spongebob(self, ctx, *, content: commands.clean_content):
        """``spongebob [msg]`` send a message in a spongebob font"""
        await self.text_prep(ctx, content[:45], "spongebob", 500, "lightblue", 100)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avenger(self, ctx, *, content: commands.clean_content):
        """``avenger [msg]`` send a message in a avenger font"""
        await self.text_prep(ctx, content[:45], "avenger", 500, "red4", 100)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def batman(self, ctx, *, content: commands.clean_content):
        """``batman [msg]`` send a message in a batman font"""
        await self.text_prep(ctx, content[:45], "batman", 500, "black", 100)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def text(self, ctx, *, content: commands.clean_content):
        """``text [msg]`` send a message in a random font"""
        await self.text_prep(ctx, content[:45], "random", 500, "random", 100)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def font(self, ctx, font, colour, *, content: commands.clean_content):
        """``font [font] [colour] [msg]`` send a message in a selected font and colour"""
        await self.text_prep(ctx, content[:45], font, 500, colour, 100)


def setup(bot):
    bot.add_cog(Fonts(bot))

