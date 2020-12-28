import os
import dbl
import discord
from discord.ext import commands

try:
    TOKEN = os.environ["TOKEN"]
    TOPGG = os.environ["TOPGG"]
    PORT = os.environ.get("PORT", 5000)
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.environ.get("BOTTOKENTEST")
    TOPGG = os.environ.get("TOPGG")
    PORT = 5000


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot

    def __init__(self, bot):
        print("setup")
        self.bot = bot
        self.dblpy = dbl.DBLClient(
            bot,
            TOPGG,
            webhook_path="/dblwebhook",
            webhook_auth="hamoodtestapi",
            webhook_port=int(PORT),
        )  # Autopost will post your guild count every 30 minutes

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print(data)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(data)

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
