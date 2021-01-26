import os
import json
from discord.ext import commands

# from modules.database import *


blacklist = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/blacklist.json"
    )
)["commandblacklist"]


def isAllowedCommand():
    async def predicate(ctx):
        return (
            ctx.channel.id not in blacklist[ctx.command.cog.__class__.__name__]
        ) or (ctx.author.id == 485138947115057162)

    return commands.check(predicate)

    # collection = json.load(open(servers_name))
    # result = search(collection, ctx.guild.id)

    # if result is None:
    #     insert_server_post(ctx.guild.id)
    #     return True

    # return result["categories"][ctx.command.cog.__class__.__name__]


# servers_name = (
#     f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/servers.json"
# )

# ["About", "Avatarmemes", "Chance", "Chemistry", "Events", "Fonts", "Fun", "Games", "General", "Images", "Math", "Memes", "Mod", "Pokemon", "Reddit", "User", "Web"]

