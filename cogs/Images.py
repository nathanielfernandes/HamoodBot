import os
from copy import copy
import random
import discord
from discord.ext import commands

from modules.image_functions import Modify, Modify_Gif
import modules.checks as checks


class Images(commands.Cog):
    """Image Manipulation `BETA`"""

    def __init__(self, bot):
        self.bot = bot
        self.direct = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        self.save_location = f"{self.direct}/tempImages"
        self.fonts = f"{self.direct}/fonts"
        self.memes = f"{self.direct}/memePics"

    # self.test123 = Modify(image_location=f"{self.memes}/furniture.png")

    async def find_image(self, ctx, member, depth):
        if member is None:
            message1 = await ctx.message.channel.history(limit=depth).find(
                lambda m: ".jpg" in str(m.attachments)
                or ".png" in str(m.attachments)
                or ".jpeg" in str(m.attachments)
                or ".gif" in str(m.attachments)
                or ".JPG" in str(m.attachments)
                or ".PNG" in str(m.attachments)
                or ".JPEG" in str(m.attachments)
                or ".GIF" in str(m.attachments)
            )

            message2 = await ctx.message.channel.history(limit=depth).find(
                lambda m: ".jpg" in str(m.content)
                or ".png" in str(m.content)
                or ".jpeg" in str(m.content)
                or ".gif" in str(m.content)
                or ".JPG" in str(m.content)
                or ".PNG" in str(m.content)
                or ".JPEG" in str(m.content)
                or ".GIF" in str(m.content)
            )

            if message1 is None:
                url = message2.content
            elif message2 is None:
                url = message1.attachments[0].url
            else:
                if message1.created_at >= message2.created_at:
                    url = message1.attachments[0].url
                else:
                    url = message2.content
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
            await ctx.send(file=discord.File(image))
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
            location=self.save_location, compression_level=10
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
