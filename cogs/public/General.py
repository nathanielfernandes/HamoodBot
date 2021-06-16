import os, re
import datetime
import random
import discord
import asyncio
from discord.ext import commands

from utils.Premium import PremiumCooldown
from modules.image_functions import randomFile, makeColor

from gtts import gTTS


class General(commands.Cog):
    """General Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.bracketed = re.compile(r"(\[.+?\])")

        self.re_entries = re.compile(r"<entry>([\s\S]*?)</entry>")
        self.re_info = re.compile(
            r"<title>([\s\S]*?)</title>|<link rel=\"alternate\" href=\"(.+)/>|<media:statistics views=\"(\d+)\"/>"
        )

        self.possiblecodes = (
            [100, 101, 102]
            + list(range(200, 109))
            + [226]
            + list(range(300, 309))
            + list(range(400, 419))
            + list(range(421, 427))
            + [428, 429, 431, 444, 451, 499]
            + list(range(500, 512))
            + [599]
        )

    @commands.command(aliases=["colour"])
    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    async def color(
        self, ctx, r: int = None, g: int = None, b: int = None, a: int = 255
    ):
        """[r] [g] [b] [a]|||Sends the color with the specified rbga values."""
        rgba = [r, g, b, a]
        for i in range(len(rgba)):
            if rgba[i] is None:
                rgba[i] = random.randint(0, 255)
            else:
                rgba[i] = abs(rgba[i])
                rgba[i] = min(rgba[i], 255)

        name = self.Hamood.save_name()
        makeColor(rgba=rgba, fp=f"{self.Hamood.filepath}/temp/{name}", size=(150, 150))

        await self.Hamood.quick_embed(
            ctx=ctx,
            footer={"text": "rgba: " + ", ".join([str(i) for i in rgba])},
            reply=True,
            image_url=f"{self.Hamood.URL}/{name}",
            color=discord.Color.from_rgb(*rgba[:-1]),
        )

    @commands.command()
    async def clap(self, ctx, *content: str):
        """<text>|||Adds clap emojis to your sentence."""
        msg = ""
        for word in content:
            msg += "**" + word + "**" + ":clap:"
        await ctx.send(msg[:1900])

    @commands.command()
    async def lengthen(self, ctx, *content: str):
        """<text>|||For when u need to fill up that essay."""

        def lengthen(word):
            halves = (word[: len(word) // 2], word[len(word) // 2 :][::-1])
            final = []
            for half in halves:
                string = ""
                for i in range(len(half)):
                    string += half[i] * (i + 1)
                final.append(string)

            return final[0] + final[1][::-1]

        await ctx.send(" ".join([lengthen(word) for word in content])[:2000])

    @commands.command()
    async def shrek(self, ctx):
        """|||The entire shrek movie as a 90 min long gif."""
        await ctx.reply("https://imgur.com/gallery/IsWDJWa")

    @commands.command(aliases=["nut", "robert"])
    @commands.bot_has_permissions(embed_links=True)
    async def nnn(self, ctx):
        """|||No Nut November Countdown."""
        embed = discord.Embed(
            title=f"No Nut November Countdown",
            color=discord.Color.from_rgb(245, 245, 220),
        )
        embed.set_footer(
            text=f"Hang in there {ctx.author}.", icon_url=ctx.author.avatar_url
        )

        today = datetime.datetime.now()
        if today.month != 11:
            embed.description = "```It is not November!```"
        else:
            end = datetime.datetime(today.year, 12, 1)

            timeLeft = end - today
            embed.description = (
                f"```{self.Hamood.pretty_dt(timeLeft.total_seconds())}```"
            )

        await ctx.send(embed=embed)

    @commands.command(aliases=["xmas"])
    @commands.bot_has_permissions(embed_links=True)
    async def christmas(self, ctx):
        """|||Christmas Countdown."""
        embed = discord.Embed(
            title=f":christmas_tree: Christmas Countdown",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Santa is comming {ctx.author}.")

        embed.set_thumbnail(
            url="https://www.animatedimages.org/data/media/359/animated-santa-claus-image-0420.gif"
        )

        today = datetime.datetime.now()
        if today.month != 12:
            embed.description = "```It is not December!```"
        else:
            end = datetime.datetime(today.year, 12, 25)

            timeLeft = end - today
            embed.description = (
                f"```{self.Hamood.pretty_dt(timeLeft.total_seconds())}```"
            )

        await ctx.send(embed=embed)

    @commands.command(aliases=["texttospeech", "say"])
    @commands.check(PremiumCooldown(prem=(2, 15, "user"), reg=(2, 15, "channel")))
    @commands.bot_has_permissions(attach_files=True)
    async def tts(self, ctx, *, content: commands.clean_content):
        """<text>|||Text to speech."""
        speech = gTTS(text=content[:600], lang="en", slow=False)
        save = (
            f"{self.Hamood.filepath}/temp/"
            + "".join([str(random.randint(0, 9)) for i in range(12)])
            + ".mp3"
        )
        speech.save(save)
        try:
            await ctx.send(file=discord.File(save))
        except Exception:
            await ctx.send("`error converting to speech`")

        os.remove(save)

    def parse_xml_entries(self, xml: str) -> [str, list]:
        try:
            entries = [
                self.Hamood.named_flatten(
                    self.re_info.findall(entry),
                    ["title", "url", "views"],
                    lambda e: e != "",
                )
                for entry in self.re_entries.findall(xml)
            ]
        except:
            return []
        else:
            return entries

    @commands.command()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def uploads(self, ctx, channel: str):
        """<youtube channel url>|||Gets the latest uploads from a channel."""
        ellipsis = lambda s: s[:35].replace("]", "").replace("[", "").replace(
            ")", ""
        ).replace("(", "").replace("|", "") + ("..." if len(s) >= 34 else "")

        channelstuff = self.Hamood.re_validChannel.search(channel)

        if channelstuff is None:
            return await ctx.send(f"`{channel}` is not a valid youtube channel!")

        soup = await self.Hamood.ahttp.get_text(url=channel)
        cID = self.Hamood.re_YoutubeID.search(soup)
        cImage = self.Hamood.re_YoutubeImage.search(soup)
        cName = self.Hamood.re_YoutubeName.search(soup)

        if cID is not None:
            cID = cID.group(1)
        else:
            return await ctx.send(f"Could not find `{channel}`")

        cImage = "temp" if cImage is None else cImage.group(1)
        cName = "NA" if cName is None else cName.group(1)

        info = await self.Hamood.ahttp.get_text(
            url=f"https://www.youtube.com/feeds/videos.xml?channel_id={cID}"
        )

        videos = self.parse_xml_entries(info)

        if len(videos) == 0:
            return await ctx.send(f"`Could not find latest uploads for '{channel}'`")

        desc = "\n".join(
            f"**{i+1}.** [**{ellipsis(videos[i]['title'])}**]({videos[i]['url']}) | `{int(videos[i]['views']):,}` views"
            for i in range(len(videos))
        )

        embed = discord.Embed(
            title=f"{cName}'s Latest Uploads",
            #  url=channel,
            color=discord.Color.from_rgb(255, 0, 0),
            description=desc,
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(url=cImage)

        return await ctx.send(embed=embed)

    @commands.command(aliases=["soggs"])
    @commands.check(PremiumCooldown(prem=(3, 5, "user"), reg=(1, 5, "user")))
    @commands.bot_has_permissions(embed_links=True)
    async def define(self, ctx, *, content: commands.clean_content):
        """<word or phrase>|||Get a difinition of a word or phrase from urban dictionary"""

        def fix_desc(desc):
            links = self.bracketed.findall(desc)
            for link in links:
                desc = desc.replace(
                    link,
                    f"{link}(https://www.urbandictionary.com/define.php?term={link.replace('[', '').replace(']', '').replace(' ', '%20')})",
                )
            return desc

        definitions = await self.Hamood.ahttp.get(
            url="https://mashape-community-urban-dictionary.p.rapidapi.com/define",
            headers={
                "x-rapidapi-key": self.Hamood.URBANDICTKEY,
                "x-rapidapi-host": self.Hamood.URBANDICTHOST,
            },
            params={"term": content},
            return_type="json",
        )

        definitions = definitions["list"]
        if len(definitions) >= 1:
            try:
                d = random.choice(definitions)
                await self.Hamood.quick_embed(
                    ctx=ctx,
                    title=f'***{d["word"]}***',
                    description=f'**{fix_desc(d["definition"])}**'
                    + f"\n\n**Example:**\n{fix_desc(d['example'])}",
                    url=d["permalink"],
                    color=discord.Color.blue(),
                    author={
                        "name": "Urban Dictionary",
                        "icon_url": "https://media.discordapp.net/attachments/741384050387714162/806013278396350464/297387706245_85899a44216ce1604c93_512.png",
                    },
                    footer={
                        "text": f"👍 {d['thumbs_up']} | 👎 {d['thumbs_down']} • by {d['author']} • {d['written_on'].split('T')[0].replace('-', '/')}"
                    },
                    reply=True,
                )
                return
            except:
                pass

        await self.Hamood.quick_embed(
            ctx=ctx,
            title=f"No Results Found For `{content}`!",
            color=discord.Color.blue(),
            author={"name": "Urban Dictionary"},
        )

    @commands.command(aliases=["statuscode"])
    async def statuscat(self, ctx, code: int = None):
        """<status-code>|||Status cats > status codes"""
        if code is None:
            code = random.choice(self.possiblecodes)
        if len(str(code)) == 3 and code in self.possiblecodes:
            await self.Hamood.quick_embed(
                ctx,
                image_url=f"https://http.cat/{code}",
                footer={"text": f"status-code: {code}"},
            )
        else:
            await self.Hamood.quick_embed(
                ctx, description=f"`{code}` is not a valid status-code."
            )


class Poll:
    def __init__(self, content, server, member):
        self.content = content.upper()
        self.results = {}

        self.content = self.content.split(", ")

        for item in self.content:
            self.results[item] = 0

        self.server = server
        self.message = None
        self.member = member
        self.embed = None
        self.timer = None
        self.voted = {}

    def update_poll(self):
        self.total = 0
        for poll in self.results:
            self.total += self.results[poll]

        self.total = 0.01 if self.total == 0 else self.total

        self.tempResults = [
            f"||{'I' * round((self.results[value] / self.total) * 100)}||"
            for value in self.results
        ]

        for i in range(len(self.tempResults)):
            if self.tempResults[i] == "||||":
                self.tempResults[i] = " "


def setup(bot):
    bot.add_cog(General(bot))
