import discord
import aiohttp
from discord.ext import commands

import modules.checks as checks


class Webhooks(commands.Cog):
    """Information Scraped From The Web"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.isAllowedCommand()
    async def subscribe(self, ctx, channel_url):
        channel_id = channel_url.strip("https://www.youtube.com/channel/")
        callback_url = "https://webhook.site/e8a15b17-8068-4d8b-893a-1c9ca3bc0e24"

        data = {
            "hub.callback": callback_url,
            "hub.topic": f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}",
            "hub.verify": "async",
            "hub.mode": "subscribe",
            "hub.verify_token": "hamood123",
        }

        async with self.bot.aioSession.post(
            "https://pubsubhubbub.appspot.com/subscribe", data=data
        ) as r:
            status = r.status
            print(status)

    @commands.command()
    @checks.isAllowedCommand()
    async def unsubscribe(self, ctx, channel_url):
        pass


def setup(bot):
    bot.add_cog(Webhooks(bot))

