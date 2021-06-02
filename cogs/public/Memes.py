import os
import random
import discord
import textwrap
from discord.ext import commands

from modules.image_functions import Modify, Modify_Gif

import modules.checks as checks


class Memes(commands.Cog):
    """Custom Text Generation Memes"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.memes = f"{self.Hamood.filepath}/memePics"
        self.save_location = f"{self.Hamood.filepath}/temp"
        self.fonts = f"{self.Hamood.filepath}/fonts"
        self.cards = {
            "billnyeCard.jpg": [[(320, 200), (355, 245)], 28],
            "caprioCard.jpg": [[(290, 152), (320, 252)], 28],
            "cucumberCard.jpg": [[(323, 120), (340, 178)], 28],
            "oldCard.jpeg": [[(93, 116), (108, 156)], 18],
            "lettuceCard.jpg": [[(350, 283), (380, 320)], 24],
            "sharpCard.png": [[(600, 465), (690, 555)], 60],
            "sharpieCard.jpg": [[(386, 245), (434, 310)], 34],
        }

    async def meme_prep(
        self, ctx, meme_image, text, coords, size, color=(0, 0, 0), wrap=12
    ):
        text = text.replace(", ", ",").split(",")
        for i in range(len(text)):
            text[i] = textwrap.wrap(text[i], width=wrap)
            for a in range(len(text[i])):
                text[i][a] += "\n"
            text[i] = " ".join(text[i])

        ext = meme_image[-3:]

        if ext == "gif":
            meme = Modify_Gif(gif_location=f"{self.memes}/{meme_image}")
        else:
            meme = Modify(image_location=f"{self.memes}/{meme_image}")
            ext = "image"

        meme.set_font(font_location=f"{self.fonts}/arialbold.ttf", font_size=size)

        for i in range(len(text)):
            getattr(meme, f"{ext}_add_text")(
                text=text[i], coordinates=coords[i], stroke_width=4, font_color=color
            )

        meme = getattr(meme, f"save_{ext}")(location=self.save_location)
        await self.Hamood.quick_embed(
            ctx=ctx,
            reply=True,
            image=meme,
            footer={"text": f"Requested by {ctx.author}"},
        )
        # meme, ext = getattr(meme, f"get_{ext}_bytes")()

        # embed = self.Hamood.quick_embed(member=ctx.author, rainbow=True, requested=True)
        # self.bot.S3.schedule_upload_bytes(
        #     file_bytes=meme, ext=ext, channel_id=ctx.channel.id, embed=embed,
        # )
        # await self.bot.S3.discordUpload(ctx, meme)

        # os.remove(meme)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def bonk(self, ctx, *, content: commands.clean_content):
        """``bonk [text1], [text2]`` adds your own text to the 'bonk' meme format"""
        await self.meme_prep(
            ctx, "bonkImage.jpg", content, [(100, 450), (900, 600)], 75
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def lick(self, ctx, *, content: commands.clean_content):
        """``lick [text1], [text2]`` adds your own text to the 'lick' meme format"""
        await self.meme_prep(ctx, "lickImage.jpg", content, [(305, 230), (40, 200)], 25)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def slap(self, ctx, *, content: commands.clean_content):
        """``slap [text1], [text2]`` adds your own text to the 'slap' meme format"""
        await self.meme_prep(
            ctx, "slapImage.jpg", content, [(580, 30), (220, 250)], 60, (255, 255, 255)
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def lookback(self, ctx, *, content: commands.clean_content):
        """``lookback [text1], [text2], [text3]`` adds your own text to the 'lookback' meme format"""
        await self.meme_prep(
            ctx, "lookBackImage.jpg", content, [(120, 285), (345, 180), (510, 300)], 30
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def our(self, ctx, *, content: commands.clean_content):
        """``our [text1], [text2]`` adds your own text to the 'our' meme format"""
        await self.meme_prep(
            ctx, "sovietImage.jpg", f"our {content}", [(325, 320), (310, 110)], 45
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def pour(self, ctx, *, content: commands.clean_content):
        """``pour [text1], [text2]`` adds your own text to the 'pour' meme format"""
        await self.meme_prep(
            ctx, "coffeeImage.jpg", content, [(50, 110), (430, 60)], 45, wrap=8
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 8, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def shoot(self, ctx, *, content: commands.clean_content):
        """``shoot [text1], [text2]`` shoot someone"""
        await self.meme_prep(
            ctx, "amongUsShoot.gif", content, [(10, 150), (170, 150)], 20, wrap=13
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def uno(self, ctx, *, content: commands.clean_content):
        """``uno [text1], [text2]`` draw 25"""
        await self.meme_prep(
            ctx, "unoImage.png", content, [(50, 170), (280, 20)], 25, wrap=15
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def present(self, ctx, *, content: commands.clean_content):
        """``present [text1]`` this is important"""
        await self.meme_prep(ctx, "presentImage.jpg", content, [(120, 65)], 22, wrap=40)

    @commands.command(aliases=["love", "val", "<3", "valentine"])
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def valentines(self, ctx, *, content: commands.clean_content):
        """``valentines [text1], [text2]`` send a valentines card <3"""
        name = random.choice(list(self.cards.keys()))
        card = self.cards[name]

        await self.meme_prep(ctx, name, content, card[0], card[1], wrap=15)


def setup(bot):
    bot.add_cog(Memes(bot))
