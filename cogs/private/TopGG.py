from discord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    # @commands.Cog.listener()
    # async def on_dbl_test(self, data):
    #     c = await self.bot.fetch_channel(749779300181606411)
    #     await c.send("got some :coffee:")

    # @commands.Cog.listener()
    # async def on_dbl_vote(self, data):
    #     await self.Hamood.Inventories.incr_all_invs(
    #         data["user"], "cheque", 1 * (2 if data["isWeekend"] else 1)
    #     )
    #     await self.Hamood.Inventories.incr_all_invs(
    #         data["user"], "blackmarket_crate", 1 * (2 if data["isWeekend"] else 1)
    #     )
    #     await self.Hamood.Inventories.incr_all_invs(
    #         data["user"], "rare_crate", 2 * (2 if data["isWeekend"] else 1)
    #     )


def setup(bot):
    bot.add_cog(TopGG(bot))
