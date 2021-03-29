import os
from copy import copy
import random
import discord
from discord.ext import commands
from math import sqrt
from modules.image_functions import Modify, Modify_Gif
import modules.checks as checks
from datetime import datetime


class Images(commands.Cog):
    """Image Manipulation `BETA`"""

    def __init__(self, bot):
        self.bot = bot
        self.save_location = f"{self.bot.filepath}/temp"
        self.fonts = f"{self.bot.filepath}/fonts"
        self.memes = f"{self.bot.filepath}/memePics"

    # self.test123 = Modify(image_location=f"{self.memes}/furniture.png")

    async def find_image(self, ctx, member, depth):
        if member is None:
            types = [".jpg", ".jpeg", ".png", ".gif", ".JPG", ".JPEG", ".PNG", ".GIF"]

            message1 = await ctx.message.channel.history(limit=depth).find(
                lambda m: any(url in str(m.attachments) for url in types)
            )

            message2 = await ctx.message.channel.history(limit=depth).find(
                lambda m: len(m.embeds) >= 1
                and m.embeds[0].to_dict().get("image") is not None
            )

            message3 = await ctx.message.channel.history(limit=depth).find(
                lambda m: any(url in str(m.content) for url in types)
            )

            s = "20120213"
            l = [
                message1.created_at
                if message1 is not None
                else datetime.strptime(s, "%Y%m%d"),
                message2.created_at
                if message2 is not None
                else datetime.strptime(s, "%Y%m%d"),
                message3.created_at
                if message3 is not None
                else datetime.strptime(s, "%Y%m%d"),
            ]
            i = l.index(max(l))
            msg = [message1, message2, message3][i]
            if msg is not None:
                if i == 0:
                    url = msg.attachments[0].url
                elif i == 1:
                    url = msg.embeds[0].to_dict().get("image")["url"]
                else:
                    url = msg.content
            else:
                url = None
        else:
            url = str(member.avatar_url).replace(".webp", ".png")

        if url is None:
            await ctx.send("`No recent images found!`")
            return None, None

        if ".gif" in url:
            return Modify_Gif(gif_url=url), "gif"

        return Modify(image_url=url), "image"

    async def send_image(self, ctx, image, msg):
        try:
            await self.bot.S3.discordUpload(ctx, image)
        except Exception:
            await ctx.send(f"`Could not {msg} image`")

        os.remove(image)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def deepfry(self, ctx, member: discord.Member = None):
        """``deepfry [@someone or send image]`` deepfries any image, tasty!"""

        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        getattr(image, f"enhance_{ext}")(contrast=10000, color=10000, sharpness=5)

        image = getattr(image, f"save_{ext}")(
            location=self.save_location, compression_level=30
        )

        await self.send_image(ctx, image, "deepfry")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def pixelate(self, ctx, amount=None):
        """``pixelate [image]`` pixelates any image"""

        image, ext = await self.find_image(ctx, None, 40)
        if image is None:
            return

        if amount is None:
            level = random.randint(10, 100)
        else:
            amount = int(amount)
            if amount > 100:
                level = 100
            elif amount < 3:
                level = 2
            else:
                level = amount

        getattr(image, f"resize_{ext}")(
            size=(int(image.image.size[0] / level), int(image.image.size[0] / level)),
            constant_resolution=True,
        )

        image = getattr(image, f"save_{ext}")(
            location=self.save_location, compression_level=50
        )

        await self.send_image(ctx, image, "pixelate")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15)
    @commands.has_permissions(attach_files=True)
    async def disgusting(self, ctx, member: discord.Member = None):
        """``disgusting [@someone or send image]`` thats disgusting!"""
        main_image, ext = await self.find_image(ctx, member, 40)
        if main_image is None:
            return

        base_image = Modify(image_location=f"{self.memes}/disgustingImage.png")
        top_image = copy(base_image)

        base_image.image_add_image(
            top_image=main_image.image,
            coordinates=(185, -20),
            top_image_size=(600, 450),
        )
        base_image.image_add_image(top_image=top_image.image)

        base_image = base_image.save_image(location=self.save_location,)

        await self.send_image(ctx, base_image, "use")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def youtube(self, ctx, *, title: commands.clean_content = None):
        """``youtube [video title]`` watch your images in youtube."""
        words = self.bot.get_cog("Fun").words

        top_image, ext = await self.find_image(ctx, None, 40)
        if top_image is None:
            return

        if title is None:
            center = " ".join(
                [random.choice(words) for i in range(random.randint(1, 7))]
            )
            title = f"{random.choice(words).capitalize()} {center}{random.choice(['!', '.', '?', ' :)'])}"

        base_image = Modify(image_location=f"{self.memes}/youtubeImage.png")
        top = copy(base_image.image)
        profile = Modify(image_url=str(ctx.author.avatar_url))
        base_image.image_add_image(
            top_image=top_image.image, coordinates=(25, 55), top_image_size=(855, 485)
        )
        base_image.image_add_image(
            top_image=profile.image, coordinates=(35, 595), top_image_size=(60, 60)
        )
        base_image.image_add_image(top_image=top)
        base_image.set_font(
            font_location=f"{self.fonts}/arialbold.ttf", font_size=30,
        )
        base_image.image_add_text(
            text=title[:50], coordinates=(30, 555), font_color=(25, 25, 25)
        )
        base_image.set_font(
            font_location=f"{self.fonts}/arialbold.ttf", font_size=15,
        )
        base_image.image_add_text(
            text=ctx.author.name, coordinates=(100, 602), font_color=(150, 150, 150)
        )
        base_image.set_font(
            font_location=f"{self.fonts}/arialbold.ttf", font_size=20,
        )
        base_image.image_add_text(
            text=f"{random.randint(1, 10000000):,} views",
            coordinates=(710, 630),
            font_color=(140, 140, 140),
        )
        base_image = base_image.save_image(location=self.save_location,)

        await self.send_image(ctx, base_image, "youtubify")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def snipe(self, ctx, member: discord.Member = None):
        """``snipe [@someone or send image]`` snipe someone or something"""
        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        getattr(image, f"resize_{ext}")(size=(256, 256))
        top_image = Modify(image_location=f"{self.memes}/scopeImage.png")
        top_image.resize_image(size=(256, 256))
        getattr(image, f"{ext}_add_image")(top_image=top_image.image)

        image = getattr(image, f"save_{ext}")(
            location=self.save_location, compression_level=100
        )

        await self.send_image(ctx, image, "snipe")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def pride(self, ctx, member: discord.Member = None):
        """``pride [@someone or send image]`` support someone or somethings pride"""
        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        # getattr(image, f"resize_{ext}")(size=(512, 512))
        top_image = Modify(image_location=f"{self.memes}/lgbtImage.png")
        top_image.resize_image(size=image.image.size)
        getattr(image, f"{ext}_add_image")(top_image=top_image.image)

        image = getattr(image, f"save_{ext}")(
            location=self.save_location, compression_level=100
        )

        await self.send_image(ctx, image, "pride")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def grayscale(self, ctx, member: discord.Member = None):
        """``grayscale [@someone or send image]`` the opposite of the pride command tbh"""
        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        image.image_grayscale()
        image = image.save_image(location=self.save_location, compression_level=100)
        await self.send_image(ctx, image, "grayscale")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 10, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def ascii(self, ctx, member: discord.Member = None):
        """``ascii [@someone or send image]`` converts an image into text"""
        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        image.regulate_size()

        x, y = image.image.size
        if x * y > 1990:
            s = sqrt(1990 / (x * y))
            image.resize_image(size=(int(x * s), int(y * s)))

        image.image_grayscale()
        text = image.image_to_ascii()

        await ctx.send(f"```{text}```")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.channel)
    @commands.has_permissions(attach_files=True)
    async def asciifull(self, ctx, member: discord.Member = None):
        """``ascii [@someone or send image]`` converts an image into text but in a larger size txt file"""
        image, ext = await self.find_image(ctx, member, 40)
        if image is None:
            return

        image.regulate_size()
        image.image_grayscale()
        text = image.image_to_ascii()

        name = "a" + "".join(random.choice("123456789") for i in range(12)) + ".txt"
        save = f"{self.save_location}/{name}"
        with open(save, "w") as f:
            f.write(text)

        await self.send_image(ctx, save, "asciify")

    # @commands.command()
    # @checks.isAllowedCommand()
    # @commands.cooldown(2, 15, commands.BucketType.channel)
    # @commands.has_permissions(attach_files=True)
    # async def edit(
    #     self, ctx, sharpness=1.0, contrast=1.0, color=1.0, brightness=1.0,
    # ):
    #     """``edit [sharpness] [contrast] [color] [brightness]`` work in progress"""
    #     image, ext = await self.find_image(ctx, None, 40)
    #     if image is None:
    #         return

    #     getattr(image, f"enhance_{ext}")(
    #         sharpness=sharpness, contrast=contrast, color=color, brightness=brightness
    #     )
    #     image = getattr(image, f"save_{ext}")(
    #         location=self.save_location, compression_level=10
    #     )

    #     await self.send_image(ctx, image, "edit")


#     @commands.command()
#     @checks.isAllowedCommand()
#     async def test(self, ctx, x, y):
#         """test [test] [test]"""

#         square = lambda x, y: [
#             x * 125,
#             y * 105,
#             (x * 125) + 125,
#             (y * 105) + 105,
#         ]

#         new = self.test123.image.crop(square(int(x), int(y)))
#         new = Modify(image=new)
#         image = new.save_image(location=self.save_location, file_format="png")

#         await self.send_image(ctx, image, "test")


# # @commands.command()
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
