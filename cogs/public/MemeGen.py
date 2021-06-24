import os, random, re
import discord, asyncio
from discord.ext import commands
from PIL import Image
from pil_stacks import Stack
from time import perf_counter
from io import BytesIO

from utils.Premium import PremiumCooldown
from modules.imageStuff.pil_presets import *


class StrMemberEmoji(commands.Converter):
    def __init__(self, n=2, require=False):
        self.n = n
        self.require = require
        self.re_member = re.compile(r"(<@!?\d+>)")
        self.re_emoji = re.compile(r"(<a?:\w+:?\d+>)")

    async def convert(self, ctx, argument):
        find_member = lambda s: self.re_member.findall(s)
        find_emoji = lambda s: self.re_emoji.findall(s)

        converters = (
            (find_member, commands.MemberConverter(), 0),
            (find_emoji, commands.PartialEmojiConverter(), 1),
        )

        args = argument.replace(", ", ",").replace(" ,", ",").split(",")
        if not isinstance(args, list):
            args = [args]

        args = args[: self.n]
        if self.require and len(args) != self.n:
            raise commands.UserInputError()

        parsed = []
        for arg in args:
            added = 0
            for pack in converters:
                search, converter, i = pack
                found = search(arg)
                if found and ((arg.strip() == found[0]) or i == 0):
                    obj = await converter.convert(ctx=ctx, argument=found[0])
                    if obj:
                        parsed.append(obj)
                        added = 1
                        break

            if not added:
                parsed.append(arg)

        return parsed[: self.n]


class MemeGen(commands.Cog):
    """Generate your own memes! :tools: `Beta`"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.memes = f"{self.Hamood.filepath}/memePics"
        self.save_location = f"{self.Hamood.filepath}/temp"
        self.fonts = f"{self.Hamood.filepath}/fonts"
        self.imagetypes = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".JPG",
            ".JPEG",
            ".PNG",
            ".GIF",
        )
        # TODO DICT STUFF

        self.BONK = Stack(
            name="bonk",
            base=f"memePics/bonkImage.jpg",
            template="templates/bonk_TEMPLATE.json",
        )
        self.LICK = Stack(
            name="lick",
            base="memePics/lickImage.jpg",
            template="templates/lick_TEMPLATE.json",
        )
        self.SLAP = Stack(
            name="slap",
            base="memePics/slapImage.jpg",
            template="templates/slap_TEMPLATE.json",
        )
        self.POUR = Stack(
            name="pour",
            base="memePics/coffeeImage.jpg",
            template="templates/pour_TEMPLATE.json",
        )
        self.SAME = Stack(
            name="stack",
            base="memePics/samePic.png",
            template="templates/difference_TEMPLATE.json",
        )
        self.LOOKBACK = Stack(
            name="lookback",
            base="memePics/lookBackImage.jpg",
            template="templates/lookback_TEMPLATE.json",
        )
        self.YOUTUBE = Stack(
            name="youtube",
            base="memePics/youtubeImage.png",
            template="templates/youtube_TEMPLATE.json",
        )

    async def search_for_image(self, ctx, depth):
        msg = await ctx.message.channel.history(limit=depth).find(
            lambda m: any(url in str(m.attachments) for url in self.imagetypes)
            or len(m.embeds) >= 1
            and m.embeds[0].to_dict().get("image") is not None
            or any(url in str(m.content) for url in self.imagetypes)
        )

        url = ""
        if msg:
            check = True
            if len(msg.attachments) > 0:
                if msg.attachments[0].size <= 4194304:
                    url = msg.attachments[0].url
                    check = False
            if len(msg.embeds) > 0:
                im = msg.embeds[0].to_dict().get("image")
                if im is not None:
                    url = im["url"]

            if url == "":
                urls = self.Hamood.re_ValidImageUrl.findall(msg.content)
                if urls:
                    url = urls[0]

            if check:
                if not url.startswith(self.Hamood.CDN_URL):
                    is_safe = await self.Hamood.ahttp.is_safe(url)
                else:
                    is_safe = True
            else:
                is_safe = True

            if is_safe:
                imagebytes = await self.Hamood.ahttp.bytes_download(url)
                try:
                    return Image.open(imagebytes)
                except:
                    await self.Hamood.quick_embed(
                        ctx,
                        title="Could not download image :(",
                        description=f"[jump1]({msg.jump_url})",
                    )
                    return
            else:
                await self.Hamood.quick_embed(
                    ctx,
                    title="Image too large or Unsafe :(",
                    description=f"[jump!]({msg.jump_url})",
                )
                return

        await self.Hamood.quick_embed(ctx, title="Could not find a recent image :(")
        return

    async def gen_kwargs(self, content: str) -> dict:
        kwargs = {}
        for i, arg in enumerate(content):
            if isinstance(arg, str):
                kwargs[f"text{i+1}"] = arg
            else:
                if isinstance(arg, discord.Member):
                    url = str(
                        arg.avatar_url_as(format="png", static_format="png", size=512)
                    )
                else:
                    url = str(arg.url)

                imagebytes = await self.Hamood.ahttp.bytes_download(url)
                kwargs[f"image{i+1}"] = (
                    Image.open(imagebytes) if imagebytes is not None else str(arg)
                )

        return kwargs

    async def send_meme(self, ctx, content, stack):
        kwargs = await self.gen_kwargs(content)
        img, dt = await self.Hamood.run_async_t(stack.generate, **kwargs)
        await self.Hamood.quick_embed(ctx=ctx, reply=True, pil_image=img, stats=dt)

    async def fetch_av(self, member: discord.Member) -> Image:
        aBytes = await member.avatar_url.read()
        return Image.open(BytesIO(aBytes))

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def bonk(self, ctx, *, content: StrMemberEmoji):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Give something or someone a good bonk!"""
        await self.send_meme(ctx, content, self.BONK)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def lick(self, ctx, *, content: StrMemberEmoji):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Thats not very hygenic."""
        await self.send_meme(ctx, content, self.LICK)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def slap(self, ctx, *, content: StrMemberEmoji):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Slap some sense into it."""
        await self.send_meme(ctx, content, self.SLAP)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def pour(self, ctx, *, content: StrMemberEmoji):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Pour someone a warm cup of whatever."""
        await self.send_meme(ctx, content, self.POUR)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def same(self, ctx, *, content: StrMemberEmoji(n=2, require=True)):
        """<text|@mention|:emoji:>, <text|@mention|:emoji:>|||Corporate wants you to find the difference."""
        await self.send_meme(ctx, content, self.SAME)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def lookback(self, ctx, *, content: StrMemberEmoji(n=3)):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:], [text|@mention|:emoji:]|||Look back at it."""
        await self.send_meme(ctx, content, self.LOOKBACK)

    @commands.command(aliases=["qoute"])
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def quote(
        self, ctx, member: discord.Member, *, content: commands.clean_content
    ):
        """<@member> <text>|||Generates a fake message from the given user."""
        av = await self.fetch_av(member)
        color = member.color.to_rgb()
        if color == (0, 0, 0):
            color = (255, 255, 255)
        img, dt = await self.Hamood.run_async_t(
            discord_quote,
            *(av, member.display_name, color, content),
        )
        await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def what(self, ctx, *, content: commands.clean_content = None):
        """[text1], [text2]|||What?, How?"""
        if content is None:
            content = "what, how"
        if "," not in content:
            content += ", "

        av = await self.search_for_image(ctx, 50)
        if av:
            img, dt = await self.Hamood.run_async_t(
                whatwhat, *(av, *content.split(","))
            )
            await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def youtube(self, ctx, *, content: commands.clean_content = None):
        """[text1], [text2]|||What?, How?"""
        if content is None:
            content = (
                " ".join(
                    random.choice(self.Hamood.RANDOMWORDS)
                    for _ in range(random.randint(3, 5))
                )
                + f" {random.choice(self.Hamood.RANDOMEMOJIS)}"
            )

        im = await self.search_for_image(ctx, 50)
        av = await self.fetch_av(ctx.author)
        if im:
            img, dt = await self.Hamood.run_async_t(
                self.YOUTUBE.generate,
                video=im,
                title=content,
                username=str(ctx.author),
                views=f"{random.randint(1, 10000000):,} views",
                pfp=av,
            )
            await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)


def setup(bot):
    bot.add_cog(MemeGen(bot))
