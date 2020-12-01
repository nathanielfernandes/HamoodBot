import os
import json
from discord.ext import commands

blacklist = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/blacklist.json"
    )
)["commandblacklist"]


def isAllowedCommand():
    async def predicate(ctx):
        return ctx.guild.id not in blacklist[ctx.command.cog.__class__.__name__]

    return commands.check(predicate)
