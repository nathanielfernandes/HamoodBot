import os
import random
import discord
from discord.ext import commands

from modules.image_functions import Edit
from modules.image_functions import Modify, Modify_Gif


class Images(commands.Cog):
    """Image Manipulation `BETA`"""

    def __init__(self, bot):
        self.bot = bot
        self.save_location = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/tempImages"
        self.fonts = (
            f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/fonts"
        )

    async def find_image(self, ctx, member, depth):
        if member is None:
            message = await ctx.message.channel.history(limit=depth).find(
                lambda m: ".jpg" in str(m.attachments)
                or ".png" in str(m.attachments)
                or ".jpeg" in str(m.attachments)
                or ".gif" in str(m.attachments)
            )
            url = message.attachments[0].url if message is not None else None
        else:
            url = str(member.avatar_url).replace(".webp", ".png")

            if url is None:
                await ctx.send("`No recent images found!`")
                return

        if ".gif" in url:
            return Modify_Gif(gif_url=url), "gif"

        return Modify(image_url=url), "image"

    async def send_image(self, ctx, image, msg):
        try:
            await ctx.send(file=discord.File(image))
        except Exception:
            await ctx.send(f"`Could not {msg} image`")

        os.remove(image)

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def deepfry(self, ctx, member: discord.Member = None):
        """``deepfry [@someone or send image]`` deepfries any image, tasty!"""

        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        getattr(image, f"enhance_{ext}")(
            sharpness=10000, contrast=10000, color=10000, brightness=10000
        )
        image = getattr(image, f"save_{ext}")(
            location=self.save_location, compression_level=10
        )

        await self.send_image(ctx, image, "deepfry")

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def pixelate(self, ctx, member: discord.Member = None):
        """``deepfry [@someone or send image]`` pixelates any image"""

        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        level = random.randint(10, 100)

        getattr(image, f"resize_{ext}")(
            size=(int(image.image.size[0] / level), int(image.image.size[0] / level)),
            constant_resolution=True,
        )

        image = getattr(image, f"save_{ext}")(
            location=self.save_location, compression_level=50
        )

        await self.send_image(ctx, image, "pixelate")

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def edit(
        self, ctx, sharpness=1.0, contrast=1.0, color=1.0, brightness=1.0,
    ):
        """``edit [sharpness] [contrast] [color] [brightness]`` work in progress"""
        image, ext = await self.find_image(ctx, None, 40)
        if image is None:
            return

        getattr(image, f"enhance_{ext}")(
            sharpness=sharpness, contrast=contrast, color=color, brightness=brightness
        )
        image = getattr(image, f"save_{ext}")(
            location=self.save_location, compression_level=10
        )

        await self.send_image(ctx, image, "edit")

    # @commands.command()
    # @commands.cooldown(3, 10, commands.BucketType.user)
    # @commands.has_permissions(attach_files=True)
    # async def toptext(self, ctx, *, text: commands.clean_content = "top text"):
    #     image = await self.find_image(ctx, None, 40)
    #     if image is None:
    #         return

    #     image.set_font(
    #         font_location=f"{self.fonts}/arialbold.ttf",
    #         font_size=image.image.size[1] // 5,
    #     )
    #     image.add_text(
    #         text=text,
    #         stroke_width=4,
    #         coordinates=(image.image.size[0] // 10, image.image.size[1] // 10),
    #     )
    #     image = image.save_image(location=self.save_location)

    #     await self.send_image(ctx, image, "add text to")


def setup(bot):
    bot.add_cog(Images(bot))
