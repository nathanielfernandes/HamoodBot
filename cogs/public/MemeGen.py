import os, random, re
import discord, asyncio
from discord.ext import commands
from PIL import Image
from pil_stacks import Stack
from time import perf_counter

from utils.Premium import PremiumCooldown


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
            (find_member, commands.MemberConverter()),
            (find_emoji, commands.PartialEmojiConverter()),
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
                search, converter = pack
                found = search(arg)
                if found:
                    obj = await converter.convert(ctx=ctx, argument=found[0])
                    if obj:
                        parsed.append(obj)
                        added = 1
                        break

            if not added:
                parsed.append(arg)

        return parsed[: self.n]


class MemeGen(commands.Cog):
    """Generate your own memes!"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.memes = f"{self.Hamood.filepath}/memePics"
        self.save_location = f"{self.Hamood.filepath}/temp"
        self.fonts = f"{self.Hamood.filepath}/fonts"

        # TODO DICT STUFF

        self.BONK = Stack(
            name="bonk",
            # base=f"memePics/bonkImage.jpg",
            # template="templates/bonk_TEMPLATE.json",
        )

        self.LICK = Stack(
            name="lick",
            # base="memePics/lickImage.jpg",
            # template="templates/lick_TEMPLATE.json",
        )

        self.SLAP = Stack(
            name="lick",
            # base="memePics/slapImage.jpg",
            # template="templates/slap_TEMPLATE.json",
        )

    async def gen_kwargs(self, content: str) -> dict:
        kwargs = {}
        for i, arg in enumerate(content):
            if isinstance(arg, str):
                kwargs[f"text{i}"] = arg
            else:
                if isinstance(arg, discord.Member):
                    url = str(
                        arg.avatar_url_as(format="png", static_format="png", size=512)
                    )
                else:
                    url = str(arg.url)
                imagebytes = await self.Hamood.ahttp.bytes_download(url)
                kwargs[f"image{i}"] = (
                    Image.open(imagebytes) if imagebytes is not None else str(arg)
                )

        return kwargs

    async def generate_meme(self, stack, *args, **kwargs):
        await self.Hamood.run_async(stack.save, *args, **kwargs)

    async def send_meme(self, ctx, content, stack):
        kwargs = await self.gen_kwargs(content)
        save_name = self.Hamood.save_name()
        kwargs["fp"] = f"{self.save_location}/{save_name}"

        tic = perf_counter()
        await self.generate_meme(stack, **kwargs)
        toc = perf_counter()

        await self.Hamood.quick_embed(
            ctx=ctx,
            reply=True,
            image_url=f"{self.Hamood.URL}/{save_name}",
            footer={
                "text": f"{ctx.command.name.title()} | Took {toc-tic:0.2f}s | Requested by {ctx.author}"
            },
        )

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.has_permissions(attach_files=True)
    async def bonk(self, ctx, *, content: StrMemberEmoji(n=2, require=True)):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Give something or someone a good bonk!"""
        await self.send_meme(ctx, content, self.BONK)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.has_permissions(attach_files=True)
    async def lick(self, ctx, *, content: StrMemberEmoji):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Thats not very hygenic."""
        await self.send_meme(ctx, content, self.LICK)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.has_permissions(attach_files=True)
    async def slap(self, ctx, *, content: StrMemberEmoji):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Slap some sense into it."""
        await self.send_meme(ctx, content, self.SLAP)


def setup(bot):
    bot.add_cog(MemeGen(bot))
