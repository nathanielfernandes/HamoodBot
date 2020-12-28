import os
import dbl
import discord
from discord.ext import commands

from utils.mongo import *

if __name__ == "__main__":
    try:
        TOKEN = os.environ["TOKEN"]
        TOPGG = os.environ["TOPGG"]
        PORT = os.environ.get("PORT", 8000)
    except KeyError:
        from dotenv import load_dotenv

        load_dotenv()
        TOKEN = os.environ.get("BOTTOKENTEST")
        TOPGG = os.environ.get("TOPGG")

    bot = commands.AutoShardedBot(
        command_prefix=commands.when_mentioned_or("."),
        case_insensitive=True,
        intents=discord.Intents().all(),
        help_command=None,
    )

    @bot.event
    async def on_message(message):
        return

    class TopGG(commands.Cog):
        """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        print("setup")
        self.bot = bot
        self.dblpy = dbl.DBLClient(
            bot,
            TOPGG,
            autopost=False,
            webhook_path="/dblwebhook",
            webhook_auth="hamoodtestapi",
            webhook_port=PORT,
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

    bot.add_cog(TopGG(bot))
    bot.run(TOKEN)
