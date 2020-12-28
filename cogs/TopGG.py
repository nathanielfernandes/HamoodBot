import dbl
import discord
from discord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot

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
