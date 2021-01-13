import os
import dbl
import discord
from discord.ext import commands
from utils.mongo import *

try:
    TOKEN = os.environ["TOKEN"]
    TOPGG = os.environ["TOPGG"]
    TOPGGAUTH = os.environ["TOPGGAUTH"]
    PORT = os.environ["PORT"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.environ.get("BOTTOKENTEST")
    TOPGG = os.environ.get("TOPGG")
    TOPGGAUTH = os.environ.get("TOPGGAUTH")
    PORT = 5000


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.dblpy = dbl.DBLClient(
            bot,
            TOPGG,
            autopost=True,
            webhook_path="/dblwebhook",
            webhook_auth=TOPGGAUTH,
            webhook_port=int(PORT),
        )  # Autopost will post your guild count every 30 minutes
        #

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        await self.bot.currency.update_all_wallets(
            data["user"], 2500 * (2 if data["isWeekend"] else 1)
        )
        if data["isWeekend"]:
            await self.bot.inventories.incr_all_invs(
                data["user"], "blackmarket_crate", 1
            )
        await self.bot.inventories.incr_all_invs(
            data["user"], "rare_crate", 2 * (2 if data["isWeekend"] else 1)
        )

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        await self.bot.currency.update_all_wallets(
            data["user"], 2500 * (2 if data["isWeekend"] else 1)
        )
        await self.bot.inventories.incr_all_invs(
            data["user"], "blackmarket_crate", 1 * (2 if data["isWeekend"] else 1)
        )
        await self.bot.inventories.incr_all_invs(
            data["user"], "rare_crate", 2 * (2 if data["isWeekend"] else 1)
        )

    # @commands.command()
    # async def bruh(self, ctx):

    #     self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5OTUxMDMxMTAxODgyMzY4MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2MzQzODMwfQ.B2IBmdp1T1CCcTagF7u8Qhh3DwgyAMJFKuOXTbVS-1A"  # set this to your DBL token
    #     self.dblpy = dbl.DBLClient(
    #         self.bot,
    #         self.token,
    #         autopost=True,
    #         webhook_path="/dblwebhook",i
    #         webhook_auth="hamoodtestapi",
    #         webhook_port=5000,
    #     )  # Autopost will post your guild count every 30 minutes

    # async def on_guild_post(self):
    #     print("Server count posted successfully")

    # @commands.Cog.listener()
    # async def on_dbl_test(self, data):
    #     print(data)

    # @commands.Cog.listener()
    # async def on_dbl_vote(self, data):
    #     print(data)


def setup(bot):
    bot.add_cog(TopGG(bot))
