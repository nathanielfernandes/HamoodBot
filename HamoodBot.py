# HamoodBot#
# date 2020/05/2
# @author Nathaniel Fernandes
"""HamoodBot is a multipurpose discord bot that has a variety of different fucntions"""

# dependancies
import os
import sys
import datetime
import random
import discord
from discord.ext import commands

sys.path.insert(
    1, f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/modules"
)

import image_functions

# bot description
description = """Hamood is a multipurpose discord bot"""

# the prefix the bot looks for before processing a message/
bot = commands.Bot(command_prefix="/", case_insensitive=True, description=description)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="with your feelings"
        )
    )
    print("-------------------")
    print(f"|Logged in as {bot.user} ({bot.user.id})|")
    print("|" + str(datetime.datetime.now()) + "|")
    print("-------------------")


responses = {
    "bye": "goodbye {0.author.mention}",
    "goodnight": "goodnight {0.author.mention}",
    "gn": "gn",
    "marco": "polo {0.author.mention}",
    "im hamood": "No your not, im hamood!",
}

file = f"{os.path.dirname(os.path.realpath(__file__))}/data/profanity.txt"
badWords = [badword[:-1] for badword in open(file, "r", encoding="utf-8").readlines()]


def profCheck(content):
    badword = list(
        dict.fromkeys([bad for bad in badWords if bad in content and len(bad) > 4])
    )
    badword += list(
        dict.fromkeys(
            [bad for bad in badWords if bad in content.split() and len(bad) <= 4]
        )
    )
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
            if "hamood" in message.content:
                uno = image_functions.Edit().randomFile(
                    f"{os.path.dirname(os.path.realpath(__file__))}/memePics/unoCards"
                )
                await message.channel.send(file=discord.File(uno))
                await message.channel.send(f"{message.author.mention} No U!")
                return
            else:
                if not nsfw:
                    if len(badword) == 1:
                        punc = "is a bad word"
                    else:
                        punc = "are bad words"

                    badword = ", ".join(badword)
                    await message.add_reaction("❌")
                    await message.channel.send(
                        f"**{message.author.mention}, ||{badword}|| {punc}, watch your profanity!**"
                    )
                    return

        elif message.content.startswith("im "):
            await message.channel.send(f"hi{message.content[2:]}, im hamood")

        elif message.content in responses:
            await message.channel.send(responses[message.content].format(message))

        await bot.process_commands(message)


@bot.command()
@commands.is_owner()
async def logout(ctx):
    """Owner Command"""
    await ctx.send("**goodbye**")
    await bot.logout()


@bot.command()
@commands.is_owner()
async def status(ctx, aType: str, *, aName: commands.clean_content):
    """Owner Command"""
    if aType == "playing":
        await bot.change_presence(activity=discord.Game(name=aName))
    elif aType == "listening":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=aName)
        )
    elif aType == "watching":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=aName)
        )
    # elif (aType == 'streaming'):
    #   await bot.change_presence(activity=discord.Streaming(name=aName, url=my_twitch_url))


@bot.command()
@commands.is_owner()
async def reload(ctx, cog):
    """Owner Command"""
    try:
        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} got reloaded")
    except Exception as e:
        print(f"{cog} cannot be loaded:")
        raise e


@bot.command()
@commands.is_owner()
async def unload(ctx, cog):
    """Owner Command"""
    try:
        bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} got unloaded")
    except Exception as e:
        print(f"{cog} cannot be unloaded:")
        raise e


@bot.command()
@commands.is_owner()
async def load(ctx, cog):
    """Owner Command"""
    try:
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} got loaded")
    except Exception as e:
        print(f"{cog} cannot be loaded:")
        raise e


# loads in all cogs
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded:")
            raise e

try:
    TOKEN = os.environ["TOKEN"]
    os.remove(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/tempImages/placeholder.txt"
    )
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.environ.get("BOTTOKEN")

bot.run(TOKEN)
