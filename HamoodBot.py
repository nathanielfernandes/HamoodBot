#Hamoods Bot#
#date 2020/05/2
#@author Nathaniel Fernandes

#dependancies
import os
import datetime
import random
import discord
from discord.ext import commands

#bot description
description = '''Hamood is ur freind'''

#the prefix the bot looks for before processing a message
bot = commands.Bot(command_prefix='', case_insensitive=True)



@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with your feelings"))
    print('-------------------')
    print(f'|Logged in as {bot.user} ({bot.user.id})|')
    print("|" + str(datetime.datetime.now()) + '|')
    print('-------------------')

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
    if (aType== 'playing'):
        await bot.change_presence(activity=discord.Game(name=aName))
    elif (aType == 'listening'):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=aName))
    elif (aType == 'watching'):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=aName))
    #elif (aType == 'streaming'):
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

#loads in all cogs
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded:")
            raise e

try:
    TOKEN = os.environ['TOKEN']
    os.remove(os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/tempImages/placeholder.txt')
except KeyError:
    from dotenv import load_dotenv
    load_dotenv()
    TOKEN = os.environ.get("BOTTOKEN")

bot.run(TOKEN)

