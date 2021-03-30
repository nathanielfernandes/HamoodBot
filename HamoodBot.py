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
import aiohttp
import discord
import asyncio
from discord.ext import commands, tasks
from modules.image_functions import randomFile
from utils.mongo import *
from utils.market import Market
from utils.helpers import pretty_time_delta
from utils.s3 import S3

if __name__ == "__main__":
    tic = time.perf_counter()

    try:
        TOKEN = os.environ["TOKEN"]
        live = True
    except KeyError:
        from dotenv import load_dotenv

        load_dotenv()
        TOKEN = os.environ.get("BOTTOKENTEST")
        live = False

    async def get_prefix(bot, message):
        if message.guild.id not in bot.prefixes_list:
            server = await bot.prefixdb.find_by_id(str(message.guild.id))
            if server is None:
                bot.prefixes_list[message.guild.id] = "."
            else:
                bot.prefixes_list[message.guild.id] = server["prefix"]
        return bot.prefixes_list.get(message.guild.id, ".")

    intents = discord.Intents().default()
    intents.members = True

    bot = commands.AutoShardedBot(
        command_prefix=get_prefix,
        case_insensitive=True,
        intents=intents,
        help_command=None,
        owner_ids={485138947115057162, 616148871499874310},
    )

    bot.islive = live
    bot.prefixes_list = {}
    bot.find_prefix = lambda guild_id: bot.prefixes_list.get(guild_id, ".")
    connected = False
    bot.timeout_list = []
    bot.filepath = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
    bot.market = Market(bot)
    bot.pretty_time_delta = pretty_time_delta
    bot.games = {}

    @bot.event
    async def on_ready():
        global connected
        bot.aioSession = aiohttp.ClientSession()
        bot.S3 = S3("hamoodbucket", TOKEN)

        bot.prefixdb = Prefixes()
        bot.leaderboards = Leaderboards()
        bot.inventories = Inventories()
        bot.currency = Currency()
        bot.members = Members()

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
        connected = True

        try:
            await bot.market.update_items.start()
        except RuntimeError:
            pass

    profane_words = [
        badword.strip("\n")
        for badword in open(f"data/profanity.txt", "r", encoding="utf-8").readlines()
    ]

    def profCheck(content):
        return max(
            [
                (len(badword) > 4 and badword in content)
                or (len(badword) <= 4 and badword in content.split())
                for badword in profane_words
            ]
        )

    @bot.event
    async def on_message(message):
        if message.guild is not None and connected:
            # checks again to make sure the bot does not reply to itself
            if (message.author.id == bot.user.id) or (
                message.author.id in bot.timeout_list
            ):
                return
            try:
                nsfw = message.channel.is_nsfw()
            except Exception:
                nsfw = False

            p = bot.find_prefix(message.guild.id)

            if profCheck((message.content).lower()):
                if (
                    "hamood" in (message.content).lower()
                    or f"<@!{bot.user.id}>" in (message.content).lower()
                ):
                    await message.channel.send(
                        f"{message.author.mention} **No U!** <a:no_u:790709588168540170>"
                    )

                if not nsfw:
                    if (message.content).startswith(p):
                        await message.add_reaction("<:profane:804446468014473246>")
                    return
            elif message.content.replace(" ", "") == f"<@!{bot.user.id}>":
                await message.channel.send(f"**The Server Prefix is `{p}`**")
                return
            elif message.content.startswith(".help") and p != ".":
                await message.channel.send(f"Use `{p}help` instead!")

            await bot.process_commands(message)

    @bot.event
    async def on_raw_reaction_add(payload):
        if payload.user_id != bot.user.id:
            if str(payload.emoji) == "<:profane:804446468014473246>":
                if (
                    payload.member.guild_permissions.manage_messages
                    or payload.user_id in [485138947115057162, 616148871499874310]
                ):
                    channel = await bot.fetch_channel(payload.channel_id)
                    msg = await channel.fetch_message(payload.message_id)

                    await msg.delete()

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

