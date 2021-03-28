import os
import discord
from discord.ext import commands

from modules.image_functions import Modify, Modify_Gif, makeColorImg
import modules.checks as checks


class Avatarmemes(commands.Cog):
    """Custom Avatar Memes"""

    def __init__(self, bot):
        self.bot = bot
        self.memes = f"{self.bot.filepath}/memePics"
        self.save_location = f"{self.bot.filepath}/temp"

    async def meme_prep(
        self, ctx, meme_image, members, positions, size, delete_og=False
    ):
        async with ctx.typing():
            members = list(members)
            if len(members) == 0:
                members.append(ctx.author)

            ext = meme_image[-3:]
            meme_save = f"{self.memes}/{meme_image}"

            if ext == "gif":
                meme = Modify_Gif(gif_location=meme_save)
            else:
                meme = Modify(image_location=meme_save)
                ext = "image"

            for i in range(len(members)):
                avatar = Modify(
                    image_url=str(members[i].avatar_url).replace(".webp", ".png")
                )

                getattr(meme, f"{ext}_add_image")(
                    top_image=avatar.image,
                    coordinates=positions[i][0],
                    top_image_size=size,
                    top_image_rotation=positions[i][1],
                )

            meme = getattr(meme, f"save_{ext}")(location=self.save_location)
            link = await self.bot.S3temp.upload(meme)

            embed = discord.Embed(
                color=ctx.author.color, timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url,
            )
            embed.set_image(url=link)

            await ctx.send(embed=embed)

        os.remove(meme)
        if delete_og:
            os.remove(meme_save)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def stonks(self, ctx, *avamember: discord.Member):
        """``stonks [@user]`` adds a tagged discord avatar to the 'stonks' meme"""

        await self.meme_prep(
            ctx, "stonksImage.jpg", avamember, [[(65, 20), 0]], (200, 200)
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def worthless(self, ctx, *avamember: discord.Member):
        """``worthless [@user]`` adds a tagged discord avatar to the 'this is worthless' meme"""
        await self.meme_prep(
            ctx, "worthlessImage.jpg", avamember, [[(490, 235), -10]], (450, 450)
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def neat(self, ctx, *avamember: discord.Member):
        """``neat [@user]`` adds a tagged discord avatar to the 'this is pretty neat' meme"""
        await self.meme_prep(
            ctx, "neatImage.jpg", avamember, [[(16, 210), 0]], (270, 270)
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def grab(self, ctx, *avamember: discord.Member):
        """``grab [@user]`` adds a tagged discord avatar to the 'grab' meme"""
        await self.meme_prep(
            ctx, "grabImage.jpg", avamember, [[(25, 265), 0]], (150, 150)
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def quiz(self, ctx, *avamember: discord.Member):
        """``quiz [@user]`` adds a tagged discord avatar to the 'quiz answer' meme"""
        await self.meme_prep(
            ctx, "quizImage.jpg", avamember, [[(355, 390), -32]], (250, 250)
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def step(self, ctx, *avamember: discord.Member):
        """``step [@user]`` adds a tagged discord avatar to the 'stepped in sh*t' meme"""
        await self.meme_prep(
            ctx, "steppedImage.png", avamember, [[(200, 640), -38]], (250, 250)
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def compare(self, ctx, *avamember: discord.Member):
        """``compare [@user1] [@user2]`` compares discord avatars"""
        if len(avamember) > 9:
            avamember = avamember[:9]

        l = len(avamember)
        scale = 200 * (10 - l)
        square = l ** 0.5
        half = l / 2
        if square.is_integer():
            x = scale * int(square)
            y = scale * int(square)
            dim = int(square)
        elif half.is_integer():
            if int(half) == 1:
                x = scale * 2
                y = scale
                dim = l
            else:
                x = scale * int(half)
                y = scale * 2
                dim = int(half)
        else:
            x = l * scale
            y = scale
            dim = l

        plate = makeColorImg(
            rgba=(255, 255, 255, 255), path=self.memes + "/", size=(x, y)
        )
        plate = plate.strip(self.memes + "/")

        coords = []
        j = 0
        k = 0
        for i in range(l):
            if i == dim or i == dim * (j + 1):
                j += 1
                k = i

            coords.append([(((i - k) * scale), j * scale), 0])

        await self.meme_prep(
            ctx, plate, avamember, coords, (scale, scale), delete_og=True
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def coffin(self, ctx, *avamember: discord.Member):
        """`coffin [text1], [text2]`"""
        await self.meme_prep(
            ctx, "coffinImage.jpg", avamember, [[(240, 160), -7]], (100, 100)
        )


def setup(bot):
    bot.add_cog(Avatarmemes(bot))

