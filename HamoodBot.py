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
from copy import copy
from modules.image_functions import randomFile
from utils.mongo import *

if __name__ == "__main__":
    tic = time.perf_counter()

    try:
        TOKEN = os.environ["TOKEN"]
        os.remove(
            f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/tempImages/placeholder.txt"
        )
        prefix = "."
        live = True
    except KeyError:
        from dotenv import load_dotenv

        load_dotenv()
        TOKEN = os.environ.get("BOTTOKENTEST")

        prefix = "/"
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
        owner_ids={317144947880886274, 485138947115057162, 616148871499874310},
    )

    bot.prefixes_list = {}
    bot.find_prefix = lambda guild_id: bot.prefixes_list.get(guild_id, ".")
    connected = False
    bot.timeout_list = []
    bot.islive = live

    every_item = json.load(open("data/items.json"))
    bot.all_items = {
        i: every_item[i] for i in every_item if every_item[i]["type"] not in ["crate"]
    }

    variation = (
        lambda: random.uniform(0.1, 1)
        if random.randint(1, 10) < 7
        else random.uniform(1, 2)
    )

    @tasks.loop(seconds=3600)
    async def update_items():
        bot.all_items = {
            i: every_item[i]
            for i in every_item
            if every_item[i]["type"] not in ["crate"]
        }

        for i in bot.all_items:
            bot.all_items[i]["price"] = round(bot.all_items[i]["value"] * variation())

        bot.common_items = {
            i: bot.all_items[i]
            for i in bot.all_items
            if bot.all_items[i]["rarity"] == "common"
        }

        bot.uncommon_items = {
            i: bot.all_items[i]
            for i in bot.all_items
            if bot.all_items[i]["rarity"] == "uncommon"
        }

        bot.rare_items = {
            i: bot.all_items[i]
            for i in bot.all_items
            if bot.all_items[i]["rarity"] == "rare"
        }

        bot.epic_items = {
            i: bot.all_items[i]
            for i in bot.all_items
            if bot.all_items[i]["rarity"] == "epic"
        }

        bot.legendary_items = {
            i: bot.all_items[i]
            for i in bot.all_items
            if bot.all_items[i]["rarity"] == "legendary"
        }

        bot.blackmarket_items = {
            i: bot.all_items[i]
            for i in bot.all_items
            if bot.all_items[i]["rarity"] == "blackmarket"
        }

        bot.dev_items = {
            i: bot.all_items[i]
            for i in bot.all_items
            if bot.all_items[i]["rarity"] == "dev"
        }

        bot.crates = {
            i: every_item[i] for i in every_item if every_item[i]["type"] == "crate"
        }

        categs = [
            (bot.common_items, random.randint(5, 8)),
            (bot.uncommon_items, random.randint(4, 7)),
            (bot.rare_items, random.randint(3, 6)),
            (bot.epic_items, random.randint(2, 5)),
            (bot.legendary_items, random.randint(0, 2)),
        ]

        bot.shop = {}
        for cat in categs:
            for i in range(cat[1]):
                k, v = random.choice(list(cat[0].items()))
                bot.shop[k] = v

        bot.all_items = copy(every_item)

        # 10800
        # asyncio.sleep(300)
        # await update_items()

    @bot.event
    async def on_ready():
        global connected
        # @ global variation

        bot.aioSession = aiohttp.ClientSession()
        # unloadList = ["Games", "Jobs", "Items", "Money"]
        # if bot.islive:
        #     for cog in unloadList:
        #         bot.unload_extension(f"cogs.{cog}")

        bot.prefixdb = Prefixes()
        bot.leaderboards = Leaderboards()
        bot.inventories = Inventories()
        bot.currency = Currency()
        bot.members = Members()

        # for cog in unloadList:
        #     bot.load_extension(f"cogs.{cog}")

        # print(bot.common_items
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

        # fp = open("/Users/nathaniel/Desktop/HamoodBot/tempImages/newyears.jpg", "rb")
        # pfp = fp.read()
        # await bot.user.edit(avatar=pfp)

        try:
            await update_items.start()
        except RuntimeError:
            pass

    responses = {
        "bye": "goodbye {0.author.mention}",
        "goodnight": "goodnight {0.author.mention}",
        "gn": "gn",
        "marco": "polo {0.author.mention}",
        "im hamood": "No your not, im hamood!",
    }

    file = f"{os.path.dirname(os.path.realpath(__file__))}/data/profanity.txt"
    profane_words = [
        badword.strip("\n") for badword in open(file, "r", encoding="utf-8").readlines()
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

            elif message.content in responses:
                await message.channel.send(responses[message.content].format(message))

            elif message.content.replace(" ", "") == f"<@!{bot.user.id}>":
                await message.channel.send(f"**The Server Prefix is `{p}`**")
                return
            elif message.content.startswith(".help") and p != ".":
                await message.channel.send(f"Use `{p}help` instead!")

            # elif (message.content).lower().startswith("im") or (
            #     message.content
            # ).lower().startswith("i'm"):
            #     await message.channel.send(
            #         f'hi {" ".join((message.content).split()[1: 10])}, im hamood'
            #     )

            await bot.process_commands(message)

    @bot.event
    async def on_raw_reaction_add(payload):
        if payload.user_id != bot.user.id:
            if str(payload.emoji) == "<:profane:804446468014473246>":
                if (
                    payload.member.guild_permissions.manage_messages
                    or payload.user_id
                    in [317144947880886274, 485138947115057162, 616148871499874310]
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

