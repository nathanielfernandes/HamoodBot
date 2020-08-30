import discord
import asyncio
from discord.ext import commands


class Mod(commands.Cog):
    """Server Moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        """``kick [@user]`` kicks a tagged member"""
        await member.kick(reason=reason)
        await ctx.send(
            f"{member.mention} was kicked by {ctx.author.mention}. [{reason}]"
        )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        """``ban [@user]`` bans a tagged member"""
        await member.ban(reason=reason)
        await ctx.send(
            f"{member.mention} was kicked by {ctx.author.mention}. [{reason}]"
        )

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount=1):
        """``clean`` deletes chat messages"""
        amount = int(amount) + 1
        if amount > 20:
            amount = 20
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=["rename"])
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(
        self, ctx, member: discord.Member = None, *, name: commands.clean_content = None
    ):
        """``nickname [@user] [newname]`` changes the nickname of a member"""
        await member.edit(nick=name) if (name != None) else None

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def channelsetup(self, ctx):
        """``channelsetup`` Creates a '+' channel which instantly creates a quick voice channel for the user that joins it"""
        category = await ctx.author.guild.create_category("Quick Channels")
        await ctx.author.guild.create_voice_channel("\u2795", category=category)
        await ctx.send(
            f"{ctx.author.mention} has setup `quick channels` in this server"
        )

    @commands.Cog.listener()
    @commands.has_permissions(manage_channels=True)
    async def on_voice_state_update(self, member, before, after):
        if before.channel is not None:
            if str(before.channel.name) == f"{member.name}'s channel":
                await before.channel.delete()

        if after.channel is not None:
            if str(after.channel.name) == "\u2795":
                channel = await member.guild.create_voice_channel(
                    f"{member.name}'s channel", category=after.channel.category
                )
                await member.move_to(channel, reason=None)
                msg = await member.guild.system_channel.send(
                    f"{member.name} created a quick channel! {await channel.create_invite()}"
                )
                await asyncio.sleep(20)
                try:
                    await msg.delete()
                except discord.errors.NotFound:
                    print("Could not delete channel!")


def setup(bot):
    bot.add_cog(Mod(bot))

