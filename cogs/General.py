import os
import datetime
import random
import discord
import asyncio
from discord.ext import commands
import aiohttp
from io import BytesIO

# import requests
from modules.image_functions import randomFile, makeColorImg
import modules.checks as checks

from gtts import gTTS

try:
    URBANDICTKEY = os.environ["URBANDICTKEY"]
    URBANDICTHOST = os.environ["URBANDICTHOST"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    URBANDICTKEY = os.environ.get("URBANDICTKEY")
    URBANDICTHOST = os.environ.get("URBANDICTHOST")


class General(commands.Cog):
    """General Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
        self.possible_responses = ["hello", "hi", "hey", "what's up"]
        self.replies = [
            "what do you want {0.author.mention}?",
            "what {0.author.mention}?",
            "huh?",
            "yeah {0.author.mention}?",
            "what's up",
        ]
        self.bad_replies = ["go away", "stop calling me"]

        self.polls = {}
        self.emojis = [
            "\U0001F7E5",
            "\U0001F7E7",
            "\U0001F7E8",
            "\U0001F7E9",
            "\U0001F7E6",
            "\U0001F7EA",
        ]

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def poll(self, ctx, *, content: commands.clean_content):
        """``poll [option1], [option2]..., [option6]`` create a poll with 2-6 options"""
        poll_id = f"{ctx.guild.id}{ctx.channel.id}"
        if len(content.split(", ")) > 6:
            await ctx.send("There is a max of 6 options for a poll!")
            return
        elif poll_id in self.polls:
            await ctx.send(
                f"This channel aldready has a poll in progress:\n{self.polls[poll_id].message.jump_url}"
            )
            return

        self.polls[poll_id] = Poll(content, ctx.guild, ctx.author)

        embed = discord.Embed(
            title=f"{ctx.author}'s Poll:",
            description="Creating... :arrows_counterclockwise:",
        )

        msg = await ctx.send(embed=embed)

        currentPoll = self.polls[poll_id]
        currentPoll.message = msg

        for i in range(len(currentPoll.results)):
            await currentPoll.message.add_reaction(self.emojis[i])
        # await currentPoll.message.add_reaction("❌")

        await self.create_poll(poll_id)
        currentPoll.timer = asyncio.create_task(self.poll_timer(poll_id))

    async def poll_timer(self, poll_id):
        await asyncio.sleep(300)
        await self.create_poll(poll_id, True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            poll_id = f"{payload.guild_id}{payload.channel_id}"
            if poll_id in self.polls:
                currentPoll = self.polls[poll_id]

                if payload.message_id == currentPoll.message.id:
                    if str(payload.emoji) in self.emojis:

                        user = str(payload.user_id)
                        key = list(currentPoll.results.keys())[
                            self.emojis.index(str(payload.emoji))
                        ]

                        if user not in currentPoll.voted:
                            currentPoll.results[key] += 1
                            currentPoll.voted[user] = key
                        else:
                            currentPoll.results[currentPoll.voted[user]] -= 1
                            currentPoll.results[key] += 1
                            currentPoll.voted[user] = key

                        await self.create_poll(poll_id)
                    # else:
                    #     if str(payload.emoji) == "❌":
                    #         currentPoll.timer.cancel()
                    #         await self.create_poll(poll_id, True)

                    await currentPoll.message.remove_reaction(
                        member=payload.member, emoji=payload.emoji
                    )

    async def create_poll(self, poll_id, delete=False):
        currentPoll = self.polls[poll_id]
        if not delete:
            currentPoll.update_poll()

            msg = ""
            for i in range(len(currentPoll.tempResults)):
                msg += f"**{list(currentPoll.results.keys())[i]}: {[round((currentPoll.results[value] / currentPoll.total) * 100, 1) for value in currentPoll.results][i]}**\n{self.emojis[i]} {currentPoll.tempResults[i]}\n"

            embed = discord.Embed(
                description=msg,
                color=currentPoll.member.color,
                timestamp=currentPoll.message.created_at,
            )
            embed.set_author(
                name=f"{currentPoll.member}'s Poll | {len(currentPoll.voted)} Votes",
                icon_url=currentPoll.member.avatar_url,
            )
            embed.set_footer(text="Polls end in 5 minutes")
            currentPoll.embed = embed
            await currentPoll.message.edit(embed=embed)
        else:
            try:
                self.polls.pop(poll_id)
                currentPoll.embed.set_footer(text="The poll has concluded.")
                await currentPoll.message.edit(embed=currentPoll.embed)
                await currentPoll.message.clear_reactions()
            except discord.errors.NotFound:
                print("Could not remove poll!")

    @commands.command(aliases=["colour"])
    @checks.isAllowedCommand()
    async def color(self, ctx, r=None, g=None, b=None, a=255):
        """``color [r] [g] [b] [a]`` sends the color with the specified rbga values"""
        rgba = [r, g, b, a]
        for i in range(len(rgba)):
            if rgba[i] is None:
                rgba[i] = random.randint(0, 255)
            else:
                rgba[i] = int(rgba[i])
                if rgba[i] < 0:
                    rgba[i] = 0
                elif rgba[i] > 255:
                    rgba[i] = 255

        img = makeColorImg(
            rgba, path=f"{self.bot.filepath}/temp", size=(150, 150), sus=(a == 69)
        )

        await self.bot.quick_embed(
            ctx=ctx,
            footer={"text": "rgba: " + ", ".join([str(i) for i in rgba])},
            reply=True,
            image=img,
            color=discord.Color.from_rgb(rgba[0], rgba[1], rgba[2]),
        )
        # bio = BytesIO()
        # img = makeColorImg(rgba)
        # img.save(bio, format="png")
        # bio = bio.getvalue()

        # embed = self.bot.quick_embed(
        #     member=ctx.author,
        #     rainbow=True,
        #     requested=True,
        #     desc="rgba: " + ", ".join([str(i) for i in rgba]),
        #     color=rgba,
        # )
        # self.bot.S3.schedule_upload_bytes(
        #     file_bytes=bio, ext="png", channel_id=ctx.channel.id, embed=embed,
        # )

    @commands.command(aliases=["hi", "hey", "yo"])
    @checks.isAllowedCommand()
    async def hello(self, ctx):
        """``greet`` greets the user"""
        await ctx.send(f"{random.choice(self.possible_responses)} {ctx.author.mention}")

    @commands.command()
    @checks.isAllowedCommand()
    async def hamood(self, ctx):
        """``hamood`` calls hamood"""
        member = ctx.author
        if self.last_member is None or self.last_member.id != member.id:
            await ctx.send(random.choice(self.replies).format(ctx))
        else:
            await ctx.send(random.choice(self.bad_replies).format(ctx))
        self.last_member = member

    @commands.command()
    @checks.isAllowedCommand()
    async def clap(self, ctx, *content: str):
        """``clap [msg]`` adds clap emojis to your sentence"""
        msg = ""
        for word in content:
            msg += "**" + word + "**" + ":clap:"
        await ctx.send(msg)

    @commands.command()
    @checks.isAllowedCommand()
    async def lengthen(self, ctx, *content: str):
        """``lengthen [sentence]`` makes words long"""

        def lengthen(word):
            halves = (word[: len(word) // 2], word[len(word) // 2 :][::-1])
            final = []
            for half in halves:
                string = ""
                for i in range(len(half)):
                    string += half[i] * (i + 1)
                final.append(string)

            return final[0] + final[1][::-1]

        await ctx.send(" ".join([lengthen(word) for word in content]))

    @commands.command()
    @checks.isAllowedCommand()
    async def clown(self, ctx, *, content: commands.clean_content = None):
        """``clown [msg]`` clown someones text"""
        if content is None:
            content = await ctx.message.channel.history(limit=5).find(
                lambda m: ".clown" not in m.content.lower()
            )
            content = content.content

        content = content.lower()
        for i in range(len(content)):
            if bool(random.getrandbits(1)):
                content = content[:i] + content[i].upper() + content[i + 1 :]
        await ctx.message.delete()
        await ctx.send(content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def repeat(self, ctx, times: int, *, content: commands.clean_content):
        """``repeat [number of messages] [msg]`` repeats your message multiple times"""
        msg = ""
        for i in range(times):
            msg += content + "\n"
        await ctx.send(msg)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def echo(self, ctx, *, content: commands.clean_content):
        """``echo [msg]`` echos your message a random amount of times"""
        for i in range(random.randint(1, 5)):
            await ctx.send(content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def no(self, ctx, content: str = None):
        """``no u`` sends an uno reverse card"""
        if content == "u" or content == "you":
            # await ctx.channel.purge(limit=1)
            uno = randomFile(folder=f"{self.bot.filepath}/memePics/unoCards")
            await ctx.send(file=discord.File(uno))

    @commands.command(aliases=["movie time"])
    async def shrek(self, ctx):
        """``shrek`` sends the entire shrek movie as a 90 min long gif"""
        await ctx.send("https://imgur.com/gallery/IsWDJWa")

    @commands.command(aliases=["nut", "robert"])
    @checks.isAllowedCommand()
    async def nnn(self, ctx):
        """``nnn`` dont nut"""
        embed = discord.Embed(
            title=f"No Nut November Countdown",
            color=discord.Color.from_rgb(245, 245, 220),
        )
        embed.set_footer(
            text=f"Hang in there {ctx.author}.", icon_url=ctx.author.avatar_url
        )

        today = datetime.datetime.now()
        if today.month != 11:
            embed.description = "It is not November"
        else:
            end = datetime.datetime(today.year, 12, 1)

            timeLeft = end - today
            embed.description = (
                f"```{self.bot.pretty_time_delta(timeLeft.total_seconds())}```"
            )

        await ctx.send(embed=embed)

    @commands.command(aliases=["xmas"])
    @checks.isAllowedCommand()
    async def christmas(self, ctx):
        """``christmas`` Christmas countdown"""
        embed = discord.Embed(
            title=f":christmas_tree: Christmas Countdown", color=discord.Color.green(),
        )
        embed.set_footer(
            text=f"Santa is comming {ctx.author}.", icon_url=ctx.author.avatar_url
        )

        embed.set_thumbnail(
            url="https://www.animatedimages.org/data/media/359/animated-santa-claus-image-0420.gif"
        )

        today = datetime.datetime.now()
        if today.month != 12:
            embed.description = "It is not December"
        else:
            end = datetime.datetime(today.year, 12, 25)

            timeLeft = end - today
            embed.description = (
                f"```{self.bot.pretty_time_delta(timeLeft.total_seconds())}```"
            )

        await ctx.send(embed=embed)

    # @commands.command(aliases=["clock"])
    # async def time(self, ctx):
    #     """``time`` sends the current time"""

    @commands.command()
    @checks.isAllowedCommand()
    async def cliffhanger(self, ctx):
        """``cliffhanger`` the day hamood died"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/767568685568753664/804052279195467796/unknown.png"
        )

    @commands.command(aliases=["texttospeech", "say"])
    @checks.isAllowedCommand()
    @commands.cooldown(2, 15, commands.BucketType.user)
    async def tts(self, ctx, *, content: commands.clean_content):
        """``tts [text]`` text to speech"""
        speech = gTTS(text=content[:600], lang="en", slow=False)
        save = (
            f"{self.bot.filepath}/temp/"
            + "".join([str(random.randint(0, 9)) for i in range(12)])
            + ".mp3"
        )
        speech.save(save)
        try:
            await ctx.send(file=discord.File(save))
        except Exception:
            await ctx.send("`error converting to speech`")

        os.remove(save)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def uploads(self, ctx, channel: str):
        """``uploads [youtube channe]`` get the last 10 videos uploaded from a channel"""
        if channel.startswith("https://www.youtube.com/"):
            if channel.startswith(
                "https://www.youtube.com/user/"
            ) or channel.startswith("https://www.youtube.com/c/"):
                soup = await self.bot.ahttp.get(url=channel, return_type="text")
                channel_id = find_id(soup)
                if channel_id is None:
                    return await ctx.send(f"`Could not find videos from '{channel}'`")
            else:
                channel_id = channel.replace("https://www.youtube.com/channel/", "")

            info = await self.bot.ahttp.get(
                url=f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
                return_type="text",
            )
            videos, name, img = sift_stuff(info)

            desc = "\n".join(
                [
                    f"[**{key}**]({value[0]})\nviews: **{int(value[1]):,}**\n"
                    for key, value in videos.items()
                ]
            )
            embed = discord.Embed(
                title=f"{name}'s Latest Uploads",
                #  url=channel,
                color=discord.Color.red(),
                description=desc,
                timestamp=ctx.message.created_at,
            )
            embed.set_thumbnail(url=img)
            return await ctx.send(embed=embed)

        return await ctx.send(f"`Could not find videos from '{channel}'`")

    @commands.command(aliases=["soggs"])
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def define(self, ctx, *, content: commands.clean_content):
        """``define [word or phrase]`` get the difinition of a word or phrase from urban dictionary"""

        def fix_desc(desc):
            d = desc
            bracketedword = ""
            start = False
            for i in d:
                if i == "[":
                    start = True
                elif i == "]":
                    start = False
                    bracketedword += i
                    d = d.replace(
                        bracketedword,
                        f"{bracketedword}(https://www.urbandictionary.com/define.php?term={bracketedword[1:-1].replace(' ', '')})",
                    )
                    bracketedword = ""
                if start:
                    bracketedword += i

            return d

        query = {"term": content}

        headers = {
            "x-rapidapi-key": URBANDICTKEY,
            "x-rapidapi-host": URBANDICTHOST,
        }

        j = await self.bot.ahttp.get(
            url="https://mashape-community-urban-dictionary.p.rapidapi.com/define",
            headers=headers,
            params=query,
            return_type="json",
        )
        # async with self.bot.aioSession.get(
        #     "https://mashape-community-urban-dictionary.p.rapidapi.com/define",
        #     headers=headers,
        #     params=query,
        # ) as r:
        #     j = await r.json()

        # r = requests.request(
        #     "GET",
        #     "https://mashape-community-urban-dictionary.p.rapidapi.com/define",
        #     headers=headers,
        #     params=query,
        # )
        if len(j) >= 1:
            try:
                definitions = j["list"]
                d = definitions[random.randint(0, len(definitions) - 1)]

                embed = discord.Embed(
                    title=d["word"].title(),
                    description=f'**{fix_desc(d["definition"])}**',
                    url=d["permalink"],
                    timestamp=ctx.message.created_at,
                    color=discord.Color.blue(),
                )

                embed.add_field(name="Example", value=fix_desc(d["example"]))

                embed.set_author(
                    name="Urban Dictionary",
                    icon_url="https://cdn.discordapp.com/attachments/741384050387714162/806013278396350464/297387706245_85899a44216ce1604c93_512.png",
                )

                embed.set_footer(text=f"👍 {d['thumbs_up']} | 👎 {d['thumbs_down']}")

                await ctx.send(embed=embed)
            except Exception:
                await ctx.send(f"`no results found for '{content}'`")


def sift_stuff(soup: str):
    name = search(soup, "<name>", "<")
    img = search(soup, '<media:thumbnail url="', '"')
    soup = soup.split("\n")
    video_titles = []
    video_links = []
    views = []

    entry = False
    for line in soup:
        if "<yt:videoId>" in line:
            video_links.append(
                f"https://www.youtube.com/watch?v={search(line, '<yt:videoId>', '<')}"
            )
        elif "<media:title>" in line:
            video_titles.append(search(line, "<media:title>", "<"))
        elif '<media:statistics views="' in line:
            views.append(search(line, '<media:statistics views="', '"'))

    return dict(zip(video_titles, zip(video_links, views))), name, img


def search(soup: str, look: str, stopper='"'):
    try:
        start = soup.index(look) + len(look)
        end = soup.index(stopper, start)
        return soup[start:end]
    except ValueError:
        return None


def find_id(soup: str):
    """Tries to find a youtube channel id"""
    result = search(soup, 'externalId":"')
    if result is None:
        result = search(soup, 'data-channel-external-id="')
    return result


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
