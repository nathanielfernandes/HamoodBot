import os
import sys
import random
import discord
import asyncio
from discord.ext import commands

sys.path.insert(
    1, f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/modules"
)

import image_functions


# Messaging cog that checks for profantiy and also provide some simple chat commands
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
    @commands.has_permissions(embed_links=True)
    async def poll(self, ctx, *, content: commands.clean_content):
        """``poll [option1], [option2]..., [option6]`` create a poll with 2-6 options"""
        poll_id = f"{ctx.guild.id}{ctx.channel.id}"
        if len(content.split(", ")) > 6:
            await ctx.send("There is a max of 6 options for a poll!")
            return
        elif poll_id in self.polls:
            await ctx.send("This channel aldready has a poll in progress")
            return

        self.polls[poll_id] = Poll(content, ctx.guild, ctx.author, None)

        embed = discord.Embed(
            title=f"{ctx.author}'s Poll:",
            description="Loading... :arrows_counterclockwise:",
        )

        msg = await ctx.send(embed=embed)

        currentPoll = self.polls[poll_id]
        currentPoll.message = msg

        for i in range(len(currentPoll.results)):
            await currentPoll.message.add_reaction(self.emojis[i])
        await currentPoll.message.add_reaction("❌")

        await self.create_poll(poll_id)
        await asyncio.sleep(300)
        await currentPoll.message.clear_reactions()
        self.polls.pop(poll_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            poll_id = f"{payload.guild_id}{payload.channel_id}"
            if poll_id in self.polls:
                currentPoll = self.polls[poll_id]

                if payload.message_id == currentPoll.message.id:
                    if str(payload.emoji) in self.emojis:
                        pick = self.emojis.index(str(payload.emoji))
                        key = list(currentPoll.results.keys())[pick]
                        currentPoll.results[key] += 1

                        await self.create_poll(poll_id)
                    else:
                        if str(payload.emoji) == "❌":
                            await currentPoll.message.clear_reactions()
                            self.polls.pop(poll_id)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id != self.bot.user.id:
            poll_id = f"{payload.guild_id}{payload.channel_id}"
            if poll_id in self.polls:
                currentPoll = self.polls[poll_id]

                if payload.message_id == currentPoll.message.id:
                    if str(payload.emoji) in self.emojis:
                        pick = self.emojis.index(str(payload.emoji))
                        key = list(currentPoll.results.keys())[pick]
                        currentPoll.results[key] -= 1

                        await self.create_poll(poll_id)

    async def create_poll(self, poll_id):
        currentPoll = self.polls[poll_id]
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
            name=f"{currentPoll.member}'s Poll:", icon_url=currentPoll.member.avatar_url
        )
        embed.set_footer(text="Poll ends in 5 minutes")
        await currentPoll.message.edit(embed=embed)

    @commands.command(aliases=["hi", "hey", "yo"])
    async def hello(self, ctx):
        """``greet`` greets the user"""
        await ctx.send(f"{random.choice(self.possible_responses)} {ctx.author.mention}")

    @commands.command()
    async def hamood(self, ctx):
        """``hamood`` calls hamood"""
        member = ctx.author
        if self.last_member is None or self.last_member.id != member.id:
            await ctx.send(random.choice(self.replies).format(ctx))
        else:
            await ctx.send(random.choice(self.bad_replies).format(ctx))
        self.last_member = member

    @commands.command()
    async def clap(self, ctx, *content: str):
        """``clap [msg]`` adds clap emojis to your sentence"""
        msg = ""
        for word in content:
            msg += "**" + word + "**" + ":clap:"
        await ctx.send(msg)

    @commands.command()
    async def repeat(self, ctx, times: int, *, content: commands.clean_content):
        """``repeat [msg]`` repeats your message multiple times"""
        msg = ""
        for i in range(times):
            msg += content + "\n"
        await ctx.send(msg)

    @commands.command()
    async def echo(self, ctx, *, content: commands.clean_content):
        """``echo [msg]`` echos your message a random amount of times"""
        for i in range(random.randint(1, 5)):
            await ctx.send(content)

    @commands.command()
    async def no(self, ctx, content: str):
        """``no u`` sends an uno reverse card"""
        if content == "u" or content == "you":
            # await ctx.channel.purge(limit=1)
            uno = image_functions.Edit().randomFile(
                f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/memePics/unoCards"
            )
            await ctx.send(file=discord.File(uno))

    @commands.command(aliases=["movie time"])
    async def shrek(self, ctx):
        """``shrek`` sends the entire shrek movie as a 90 min long gif"""
        await ctx.send("https://imgur.com/gallery/IsWDJWa")


class Poll:
    def __init__(self, content, server, member, msg):
        self.content = content.upper()
        self.results = {}

        self.content = self.content.split(", ")

        for item in self.content:
            self.results[item] = 0

        self.server = server
        self.message = msg
        self.member = member

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
