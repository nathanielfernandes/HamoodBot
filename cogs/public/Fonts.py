import os
import discord
import random
import json
from discord.ext import commands
from PIL import ImageFont
from modules.imageStuff.pil_presets import betterText
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
            "arial": ("arialbold.ttf", "random"),
            "minec": ("Minecraft.ttf", "random"),
            "undertale": ("DTM-Sans.ttf", "random"),
            "gta": ("pricedow.ttf", "random"),
            "enchant": ("minecraft-enchantment.ttf", "random"),
            "unknown": ("unown.ttf", "random"),
            "pokefont": ("Pokemon_Solid.ttf", "random"),
            "sega": ("SEGA.TTF", "random"),
            "spongebob": ("Krabby_Patty.ttf", "random"),
            "avangers": ("AVENGEANCE_HEROIC_AVENGER_BD.ttf", "random"),
            "batman": ("BATMAN.TTF", "random"),
        }

        # TODO find out which is better
        for key in self.FontCommands:
            self.FontCommands[key] += (
                "",
                # ImageFont.truetype(f"{self.fonts}/{self.FontCommands[key][0]}", 100),
            )

        self.allFonts = [
            value[0]
            for value in list(self.FontCommands.values())
            if value[0]
            not in (
                "minecraft-enchantment.ttf",
                "unown.ttf",
                "AVENGEANCE_HEROIC_AVENGER_BD.ttf",
            )
        ]
        self.allColors = list(self.colorDict.values())

    def addfontcommands(self):
        for name in self.FontCommands:

            @commands.command(
                name=name,
                help=f"<text>|||See your message in a `{name}` font.",
                aliases=["text"] if name == "arial" else [],
            )
            @commands.check(PremiumCooldown(prem=(1, 2.5, "user"), reg=(1, 5, "user")))
            @commands.bot_has_permissions(attach_files=True, embed_links=True)
            async def cmd(
                self, ctx, *, content: commands.clean_content(fix_channel_mentions=True)
            ):
                await self.gen_text(ctx, content, self.FontCommands[ctx.command.name])

            cmd.cog = self
            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            self.bot.add_command(cmd)

    async def gen_text(self, ctx, text, pack, send=True):
        all_es = self.Hamood.re_emoji.findall(text)[:20]
        ttext = str(text)
        for e in all_es:
            ttext = ttext.replace(e, "O")

        if len(ttext) > 50:
            text = text[:50]

        if len(text) == 0:
            raise commands.UserInputError()

        fontname, color, font = pack
        if fontname == "random":
            font = random.choice(self.allFonts)
        elif fontname in self.FontCommands:
            font = self.FontCommands[fontname][0]
        else:
            font = fontname

        if color == "random":
            color = self.Hamood.pastel_color()
        elif color not in self.colorDict:
            color = (255, 255, 255)
        else:
            color = tuple(self.colorDict[color])

        font = ImageFont.truetype(f"{self.fonts}/{font}", 100)
        # fp, url = self.Hamood.cdnsave(ext="png")
        img = await self.Hamood.run_async(betterText, *(text, font, color))
        # await self.Hamood.run_async(makeText, *(text, font, 200, color, fp))

        if len(color) > 3:
            color = color[:-1]

        if send:
            await self.Hamood.quick_embed(
                ctx=ctx,
                pil_image=img,
                color=discord.Color.from_rgb(*color),
            )
        else:
            return img, color

    @commands.command()
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    @commands.check(PremiumCooldown(prem=(2, 2.5, "user"), reg=(2, 5, "user")))
    async def randomtext(
        self, ctx, *, content: commands.clean_content(fix_channel_mentions=True)
    ):
        """<randomtext>|||See your message in a random font."""
        await self.gen_text(ctx, content, ("random", "random", ""))

    @commands.command()
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    @commands.check(PremiumCooldown(prem=(2, 2.5, "user"), reg=(2, 5, "user")))
    async def font(
        self,
        ctx,
        font,
        colour,
        *,
        content: commands.clean_content(fix_channel_mentions=True),
    ):
        """<font> <color> <text>|||See your message with any font or color."""
        await self.gen_text(ctx, content, (font, colour, ""))


def setup(bot):
    cog = Fonts(bot)
    bot.add_cog(cog)
    cog.addfontcommands()
