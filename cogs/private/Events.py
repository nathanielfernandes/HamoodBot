import os, time
import discord
from discord.ext import commands


class Events(commands.Cog):
    """Handles Any Discord Events"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.tic = time.perf_counter()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            if str(payload.emoji) == "<:profane:804446468014473246>":
                if (
                    payload.member.guild_permissions.manage_messages
                    or payload.user_id in [485138947115057162, 616148871499874310,]
                ):
                    channel = await self.Hamood.bot.fetch_channel(payload.channel_id)
                    msg = await channel.fetch_message(payload.message_id)

                    await msg.delete()

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     if channel is not None:
    #         await channel.send(f"Welcome {member.mention}!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.id == self.bot.user.id:
            return

        await self.Hamood.Leaderboards.delete_member(member.guild.id, member.id)
        await self.Hamood.Currency.delete_member(member.guild.id, member.id)
        await self.Hamood.Inventories.delete_member(member.guild.id, member.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.Hamood.Leaderboards.delete_by_id(guild.id)
        await self.Hamood.Currency.delete_by_id(guild.id)
        await self.Hamood.Inventories.delete_by_id(guild.id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).embed_links:
                embed = discord.Embed(
                    title=f"Hi {guild}, im Hamood!",
                    description=f"My command prefix is '`.`', use `.help` or [**click here**](https://hamood.app/commands) to get started.",
                )

                embed.add_field(
                    name="Website", value="[**click here**](https://hamood.app/)",
                )
                embed.add_field(
                    name="For bugs, further help or suggestions",
                    value="You can message me on discord\n`nathan#3724`",
                )

                await channel.send(embed=embed)
            break


def setup(bot):
    bot.add_cog(Events(bot))

