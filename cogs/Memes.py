import os
import discord
import textwrap
from discord.ext import commands

from modules.image_functions import Edit


class Memes(commands.Cog):
    """Custom Text Generation Memes"""

    def __init__(self, bot):
        self.bot = bot
        self.direct = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        self.edit = Edit(
            f"{self.direct}/memePics",
            f"{self.direct}/tempImages",
            f"{self.direct}/fonts",
        )

    async def textMemePrep(
        self, ctx, text, coords, font, colour, source, wrap=12, gif=False
    ):
        async with ctx.typing():

            text = text.split(", ")

            for i in range(len(text)):
                text[i] = textwrap.wrap(text[i], width=wrap)
                for a in range(len(text[i])):
                    text[i][a] += "\n"
                text[i] = " ".join(text[i])

            for i in range(len(coords)):
                coords[i].append(text[i])

            name = self.edit.randomNumber()
            if gif:
                name = str(name) + ".gif"
                meme = self.edit.gif_addText(
                    source, font, colour, coords, name, "arialbold.ttf"
                )
            else:
                name = str(name) + ".jpg"
                meme = self.edit.addText(
                    source, font, colour, coords, name, "arialbold.ttf"
                )
            # await ctx.message.delete()
            await ctx.send(file=discord.File(meme))

        os.remove(meme)

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def bonk(self, ctx, *, content: commands.clean_content):
        """``bonk [text1], [text2]`` adds your own text to the 'bonk' meme format"""
        await self.textMemePrep(
            ctx, content, [[(250, 450)], [(1050, 600)]], 75, "BLACK", "bonkImage.jpg"
        )

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def lick(self, ctx, *, content: commands.clean_content):
        """``lick [text1], [text2]`` adds your own text to the 'lick' meme format"""
        await self.textMemePrep(
            ctx, content, [[(320, 220)], [(75, 200)]], 35, "BLACK", "lickImage.jpg"
        )

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def slap(self, ctx, *, content: commands.clean_content):
        """``slap [text1], [text2]`` adds your own text to the 'slap' meme format"""
        await self.textMemePrep(
            ctx, content, [[(580, 30)], [(220, 250)]], 60, "WHITE", "slapImage.jpg"
        )

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def lookback(self, ctx, *, content: commands.clean_content):
        """``lookback [text1], [text2], [text3]`` adds your own text to the 'lookback' meme format"""
        await self.textMemePrep(
            ctx,
            content,
            [[(120, 285)], [(360, 180)], [(525, 250)]],
            30,
            "BLACK",
            "lookBackImage.jpg",
            14,
        )

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def our(self, ctx, *, content: commands.clean_content):
        """``our [text1], [text2]`` adds your own text to the 'our' meme format"""
        content = "our " + content + ",  "
        await self.textMemePrep(
            ctx, content, [[(325, 320)], [(310, 110)]], 45, "BLACK", "sovietImage.jpg"
        )

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def pour(self, ctx, *, content: commands.clean_content):
        """``pour [text1], [text2]`` adds your own text to the 'pour' meme format"""
        await self.textMemePrep(
            ctx, content, [[(50, 110)], [(430, 60)]], 45, "BLACK", "coffeeImage.jpg", 8
        )

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def shoot(self, ctx, *, content: commands.clean_content):
        """``shoot [text1], [text2]`` shoot someone"""
        await self.textMemePrep(
            ctx,
            content,
            [[(80, 245)], [(240, 245)]],
            20,
            "WHITE",
            "amongUsShoot.gif",
            9,
            True,
        )


def setup(bot):
    bot.add_cog(Memes(bot))
