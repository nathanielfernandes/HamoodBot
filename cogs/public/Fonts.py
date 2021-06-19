import os
import discord
import random
import json
from discord.ext import commands

from modules.image_functions import makeText
from utils.Premium import PremiumCooldown


class Fonts(commands.Cog):
    """Send Messages With Cool Fonts"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.colorDict = json.load(open(f"{self.Hamood.filepath}/data/colours.json"))
        self.save_location = f"{self.Hamood.filepath}/temp"
        self.fonts = f"{self.Hamood.filepath}/fonts"

        self.FontCommands = {
            "arial": ("arialbold.ttf", "black"),
            "minec": ("Minecraft.ttf", "yellow2"),
            "undertale": ("DTM-Sans.ttf", "white"),
            "morty": ("get_schwhifty.ttf", "green1"),
            "gta": ("pricedow.ttf", "white"),
            "enchant": ("minecraft-enchantment.ttf", "white"),
            "unknown": ("unown.ttf", "black"),
            "pokefont": ("Pokemon_Solid.ttf", "steelblue2"),
            "sega": ("SEGA.TTF", "navy"),
            "spongebob": ("Krabby_Patty.ttf", "lightblue"),
            "avangers": ("AVENGEANCE_HEROIC_AVENGER_BD.ttf", "red4"),
            "batman": ("BATMAN.TTF", "black"),
        }

        self.allFonts = [
            value[0]
            for value in list(self.FontCommands.values())
            if value[0] not in ("minecraft-enchantment.ttf", "unown.ttf")
        ]
        self.allColors = list(self.colorDict.values())

    def addfontcommands(self):
        for name in self.FontCommands:

            @commands.command(
                name=name, help=f"<text>|||See your message in a '{name}` font.",
            )
            @commands.check(PremiumCooldown(prem=(1, 2.5, "user"), reg=(1, 5, "user")))
            async def cmd(self, ctx, *, content: commands.clean_content):
                await self.gen_text(ctx, content, self.FontCommands[ctx.command.name])

            cmd.cog = self
            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            self.bot.add_command(cmd)

    async def gen_text(self, ctx, text, pack, send=True):
        text = text[:45]
        if len(text) == 0:
            raise commands.UserInputError()

        font, color = pack
        if font == "random":
            font = random.choice(self.allFonts)
        elif font in self.FontCommands:
            font = self.FontCommands[font][0]
        if color == "random":
            color = self.Hamood.pastel_color()
        elif color not in self.colorDict:
            color = (255, 255, 255)
        else:
            color = tuple(self.colorDict[color])

        font = f"{self.fonts}/{font}"
        name = self.Hamood.save_name()
        await self.Hamood.run_async(
            makeText, *(text, font, 200, color, f"{self.save_location}/{name}")
        )
        url = f"{self.Hamood.CDN_URL}/{name}"

        if send:
            await self.Hamood.quick_embed(
                ctx=ctx, image_url=url, color=discord.Color.from_rgb(*color),
            )
        else:
            return url, color

    @commands.command()
    @commands.check(PremiumCooldown(prem=(1, 2.5, "user"), reg=(1, 5, "user")))
    async def text(self, ctx, *, content: commands.clean_content):
        """<text>|||See your message in a random font."""
        await self.gen_text(ctx, content, ("random", "random"))

    @commands.command()
    @commands.check(PremiumCooldown(prem=(1, 2.5, "user"), reg=(1, 5, "user")))
    async def font(self, ctx, font, colour, *, content: commands.clean_content):
        """<font> <color> <text>|||See your message with any font or color."""
        await self.gen_text(ctx, content, (font, colour))


def setup(bot):
    cog = Fonts(bot)
    bot.add_cog(cog)
    cog.addfontcommands()
