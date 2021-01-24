import os
import dbl
import discord
from discord.ext import commands
from utils.mongo import *

try:
    TOPGG = os.environ["TOPGG"]
    TOPGGAUTH = os.environ["TOPGGAUTH"]
    PORT = os.environ["PORT"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
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
            # autopost=True,
            webhook_path="/dblwebhook",
            webhook_auth=TOPGGAUTH,
            webhook_port=int(PORT),
        )

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        c = await self.bot.fetch_channel(749779300181606411)
        await c.send("got some :coffee:")

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


def setup(bot):
    bot.add_cog(TopGG(bot))
