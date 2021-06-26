import os, random, re
import discord, asyncio
from discord.ext import commands
from PIL import Image
from pil_stacks import Stack
from time import perf_counter
from io import BytesIO
from typing import Union

from utils.Premium import PremiumCooldown
from modules.imageStuff.pil_presets import *


class StrMemberEmoji(commands.Converter):
    def __init__(
        self,
        n=2,
        require=False,
    ):
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
                if found and (arg.strip() == found[0]):
                    obj = await converter.convert(ctx=ctx, argument=found[0])
                    if obj:
                        parsed.append(obj)
                        added = 1
                        break

            if not added:
                parsed.append(
                    await commands.clean_content(
                        use_nicknames=True, fix_channel_mentions=True
                    ).convert(ctx, arg)
                )

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
        self.COFFIN = Stack(
            name="coffin",
            base="memePics/coffinImage.jpg",
            template="templates/coffin_TEMPLATE.json",
        )
        self.NEAT = Stack(
            name="neat",
            base="memePics/neatImage.jpg",
            template="templates/neat_TEMPLATE.json",
        )
        self.GRAB = Stack(
            name="grab",
            base="memePics/grabImage.jpg",
            template="templates/grab_TEMPLATE.json",
        )
        self.PRESENT = Stack(
            name="present",
            base="memePics/presentImage.jpg",
            template="templates/present_TEMPLATE.json",
        )
        self.WORTHLESS = Stack(
            name="worthless",
            base="memePics/worthlessImage.jpg",
            template="templates/worthless_TEMPLATE.json",
        )

        self.CHOICES = Stack(
            name="choices",
            base="memePics/choiceImage.png",
            template="templates/choices_TEMPLATE.json",
        )
        self.DISGUSTING = Stack(
            name="disgusting",
            base="memePics/disgustingImage.png",
            template="templates/disgusting_TEMPLATE.json",
        )
        self.SWERVE = Stack(
            name="swerve",
            base="memePics/swerveImage.jpg",
            template="templates/zoom_TEMPLATE.json",
        )
        self.SNIPE = Stack(
            name="snipe",
            base="memePics/scopeImage.png",
            template="templates/snipe_TEMPLATE.json",
        )
        self.STONKS = Stack(
            name="stonks",
            base="memePics/stonksImage.jpg",
            template="templates/stonks_TEMPLATE.json",
        )
        self.UNO = Stack(
            name="uno",
            base="memePics/unoImage.png",
            template="templates/uno_TEMPLATE.json",
        )
        self.STEPPED = Stack(
            name="stepped",
            base="memePics/steppedImage.png",
            template="templates/stepped_TEMPLATE.json",
        )
        self.NOTE = Stack(
            name="note",
            base="memePics/quizImage.jpg",
            template="templates/note_TEMPLATE.json",
        )
        self.TSHIRT = Stack(
            name="tshirt",
            base="memePics/tshirtImage.png",
            template="templates/tshirt_TEMPLATE.json",
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
                if msg.attachments[0].size <= 8388608:
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
        cache = {}
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

                if url not in cache:
                    imagebytes = await self.Hamood.ahttp.bytes_download(url)
                    pil = Image.open(imagebytes) if imagebytes is not None else str(arg)
                    cache[url] = pil
                else:
                    pil = cache[url]
                kwargs[f"image{i+1}"] = pil

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

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def coffin(
        self, ctx, content: Union[discord.Member, discord.PartialEmoji] = None
    ):
        """[@mention|:emoji:]|||Okay, get in."""
        content = ctx.author if content is None else content
        await self.send_meme(ctx, [content], self.COFFIN)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def grab(
        self, ctx, content: Union[discord.Member, discord.PartialEmoji] = None
    ):
        """[@mention|:emoji:]|||You belong to it now."""
        content = ctx.author if content is None else content
        await self.send_meme(ctx, [content], self.GRAB)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def worthless(
        self, ctx, content: Union[discord.Member, discord.PartialEmoji] = None
    ):
        """[@mention|:emoji:]|||That's worthless."""
        content = ctx.author if content is None else content
        await self.send_meme(ctx, [content, content], self.WORTHLESS)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def present(self, ctx, *, content: StrMemberEmoji(n=1, require=True) = None):
        """<text|@mention|:emoji:|||Yeah this is presentable."""
        if content is None:
            im = await self.search_for_image(ctx, 50)
            if im:
                img, dt = await self.Hamood.run_async_t(
                    self.PRESENT.generate,
                    image1=im,
                )
                await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)
        else:
            await self.send_meme(ctx, content, self.PRESENT)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def choices(self, ctx, *, content: StrMemberEmoji(n=3, require=True)):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:], [text|@mention|:emoji:]|||So many choices, so little time."""
        await self.send_meme(ctx, content, self.CHOICES)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def disgusting(self, ctx):
        """|||It speaks for itself."""
        im = await self.search_for_image(ctx, 50)
        if im:
            img, dt = await self.Hamood.run_async_t(
                self.DISGUSTING.generate, image1=im, image2=self.DISGUSTING.image
            )
            await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def swerve(self, ctx, *, content: StrMemberEmoji(n=3, require=True)):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:], [text|@mention|:emoji:]|||Which way are you gonna go."""
        await self.send_meme(ctx, content, self.SWERVE)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def snipe(
        self, ctx, content: Union[discord.Member, discord.PartialEmoji] = None
    ):
        """[@mention|:emoji:]|||Snipe someone or something."""
        if content is None:
            im = await self.search_for_image(ctx, 50)
            if im:
                img, dt = await self.Hamood.run_async_t(
                    self.SNIPE.generate, image1=im, image2=self.SNIPE.image
                )
                await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)
        else:
            await self.send_meme(ctx, content, self.SNIPE)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def stonks(
        self, ctx, content: Union[discord.Member, discord.PartialEmoji] = None
    ):
        """[@mention|:emoji:]|||Stonks!"""
        content = ctx.author if content is None else content
        await self.send_meme(ctx, [content], self.STONKS)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def uno(self, ctx, *, content: StrMemberEmoji):
        """<text|@mention|:emoji:>, [text|@mention|:emoji:]|||Draw 25 or..."""
        await self.send_meme(ctx, content, self.UNO)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def stepped(
        self, ctx, content: Union[discord.Member, discord.PartialEmoji] = None
    ):
        """[@mention|:emoji:]|||Just stepped in sh#$&."""
        content = ctx.author if content is None else content
        await self.send_meme(ctx, [content], self.STEPPED)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def note(self, ctx, *, content: StrMemberEmoji(n=1, require=True) = None):
        """<text|@mention|:emoji:|||What is this."""
        if content is None:
            im = await self.search_for_image(ctx, 50)
            if im:
                img, dt = await self.Hamood.run_async_t(
                    self.NOTE.generate,
                    image1=im,
                )
                await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)
        else:
            await self.send_meme(ctx, content, self.NOTE)

    @commands.command(aliases=["shirt", "tradam"])
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def tshirt(self, ctx, *, content: StrMemberEmoji(n=1, require=True) = None):
        """<text|@mention|:emoji:|||Put it on a tshirt."""
        if content is None:
            im = await self.search_for_image(ctx, 50)
            if im:
                img, dt = await self.Hamood.run_async_t(
                    self.TSHIRT.generate,
                    image1=im,
                )
                await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)
        else:
            await self.send_meme(ctx, content, self.TSHIRT)

    @commands.command(aliases=["gay", "pride"])
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def rainbow(self, ctx, content: Union[discord.Member] = None):
        """[@member]|||Rainbow hmmm."""
        if content is None:
            im = await self.search_for_image(ctx, 50)
        else:
            im = await self.fetch_av(content)

        if im:
            img, dt = await self.Hamood.run_async_t(rainbowfy, image=im)
            await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def stepped(
        self, ctx, content: Union[discord.Member, discord.PartialEmoji] = None
    ):
        """[@mention|:emoji:]|||Just stepped in sh#$&."""
        content = ctx.author if content is None else content
        await self.send_meme(ctx, [content], self.STEPPED)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def youtube(
        self,
        ctx,
        *,
        content: commands.clean_content(
            use_nicknames=True, fix_channel_mentions=True, remove_markdown=True
        ) = None,
    ):
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

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def ascii(self, ctx, content: Union[discord.Member] = None):
        """[@member]|||Converts images to text."""
        if content is None:
            im = await self.search_for_image(ctx, 50)
        else:
            im = await self.fetch_av(content)

        if im:
            img, dt = await self.Hamood.run_async_t(image_to_ascii, image=im)
            await ctx.reply(content=f"```{img}```", mention_author=False)

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "channel")))
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def meme(
        self,
        ctx,
        *,
        content: commands.clean_content(
            use_nicknames=True, fix_channel_mentions=True, remove_markdown=True
        ) = None,
    ):
        """[toptext], [bottomtext]|||Your standard meme format."""
        if content is None:
            content = "TOPTEXT, BOTTOMTEXT"
        if "," not in content:
            content += ", "

        im = await self.search_for_image(ctx, 50)
        if im:
            img, dt = await self.Hamood.run_async_t(
                standardmeme, *(im, *content.split(","))
            )
            if img:
                await self.Hamood.quick_embed(ctx, pil_image=img, stats=dt)
            else:
                await self.Hamood.quick_embed(
                    ctx,
                    title="Could Not Generate Meme :(",
                    description="Image dimensions could have been too weird.",
                )

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
    async def what(
        self,
        ctx,
        *,
        content: commands.clean_content(
            use_nicknames=True, fix_channel_mentions=True, remove_markdown=True
        ) = None,
    ):
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


def setup(bot):
    bot.add_cog(MemeGen(bot))
