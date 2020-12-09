# HamoodBot#
# date 2020/05/2
# @author Nathaniel Fernandes
"""HamoodBot is a multipurpose discord bot that has a variety of different functions"""

# dependancies
import time
import os
import json
import datetime
import random
import discord
from discord.ext import commands

from modules.image_functions import randomFile
from utils.mongo import Leaderboards


if __name__ == "__main__":
    tic = time.perf_counter()

    try:
        TOKEN = os.environ["TOKEN"]
        os.remove(
            f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/tempImages/placeholder.txt"
        )
        prefix = "."
    except KeyError:
        from dotenv import load_dotenv

        load_dotenv()
        TOKEN = os.environ.get("BOTTOKENTEST")
        prefix = "/"

    bot = commands.AutoShardedBot(
        command_prefix=commands.when_mentioned_or(prefix),
        case_insensitive=True,
        intents=discord.Intents().all(),
        help_command=None,
    )

    @bot.event
    async def on_ready():
        bot.leaderboards = Leaderboards()

        toc = time.perf_counter()

        print("-------------------")
        print(f"|Logged in as {bot.user} ({bot.user.id})|")
        print("|" + str(datetime.datetime.now()) + "|")
        print("-------------------")
        print(f"Took {toc-tic:0.2f} seconds")
        print("-------------------")

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{sum([len(g.members) for g in bot.guilds])} Users",
            )
        )

    responses = {
        "bye": "goodbye {0.author.mention}",
        "goodnight": "goodnight {0.author.mention}",
        "gn": "gn",
        "marco": "polo {0.author.mention}",
        "im hamood": "No your not, im hamood!",
    }

    file = f"{os.path.dirname(os.path.realpath(__file__))}/data/profanity.txt"
    badWords = [
        badword.strip("\n") for badword in open(file, "r", encoding="utf-8").readlines()
    ]

    def profCheck(content):
        badword = [bad for bad in badWords if bad in content and len(bad) > 4]
        badword += [bad for bad in badWords if bad in content.split() and len(bad) <= 4]
        badword = list(dict.fromkeys(badword))

        profane = True if badword else False
        return profane, badword

    @bot.event
    async def on_message(message):
        if message.guild is not None:
            # checks again to make sure the bot does not reply to itself
            if message.author.id == bot.user.id:
                return
            try:
                nsfw = message.channel.is_nsfw()
            except Exception:
                nsfw = False

            profane, badword = profCheck((message.content).lower())

            if profane:
                if not nsfw:
                    await message.add_reaction("<:trash:783097450461397052>")
                    return

            elif message.content in responses:
                await message.channel.send(responses[message.content].format(message))
            elif message.content.startswith("im "):
                await message.channel.send(f"hi{message.content[2:]}, im hamood")

            await bot.process_commands(message)

    @bot.event
    async def on_raw_reaction_add(payload):
        if payload.user_id != bot.user.id:
            if str(payload.emoji) == "<:trash:783097450461397052>":
                if payload.member.guild_permissions.manage_messages:
                    channel = await bot.fetch_channel(payload.channel_id)
                    msg = await channel.fetch_message(payload.message_id)

                    await msg.delete()

    @bot.command()
    @commands.is_owner()
    async def logout(ctx):
        """logs hamood out"""
        await ctx.send("**goodbye**")
        await bot.logout()

    @bot.command()
    @commands.is_owner()
    async def status(ctx, aType: str, uRL: str, *, aName: commands.clean_content):
        """lets me change hamoods status"""
        if aType == "playing":
            await bot.change_presence(activity=discord.Game(name=aName))
        elif aType == "listening":
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, name=aName
                )
            )
        elif aType == "watching":
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=aName
                )
            )
        elif aType == "streaming":
            await bot.change_presence(activity=discord.Streaming(name=aName, url=uRL))

    @bot.command()
    @commands.is_owner()
    async def reload(ctx, cog):
        """reloads the requested cog"""
        try:
            bot.unload_extension(f"cogs.{cog}")
            bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got reloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded`")
            raise e

    @bot.command()
    @commands.is_owner()
    async def unload(ctx, cog):
        """unloads the requested cog"""
        try:
            bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got unloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be unloaded:`")
            raise e

    @bot.command()
    @commands.is_owner()
    async def load(ctx, cog):
        """loads the requested cog"""
        try:
            bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got loaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded:`")
            raise e

    # loads in all cogs
    print("-------------------")
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                bot.load_extension(cog)
                print(f"{cog} Loaded!")
            except Exception as e:
                print(f"{cog} cannot be loaded:")
                raise e
    print("-------------------")

    bot.run(TOKEN)

