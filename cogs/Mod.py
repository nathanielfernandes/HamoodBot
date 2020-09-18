import discord
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
            f"{member.mention} was kicked by {ctx.author.mention} | reason `{reason}`"
        )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        """``ban [@user]`` bans a tagged member"""
        await member.ban(reason=reason)
        await ctx.send(
            f"{member.mention} was kicked by {ctx.author.mention} | reason: `{reason}`"
        )

    @commands.command()
    async def prunes(self, ctx, days: int = 7):
        """``prunes [days]`` returns how many roleless members have not been active on the server"""
        prunes = await ctx.guild.estimate_pruned_members(days=days)
        await ctx.send(
            f"`{prunes} roleless users have not been active for {days} days`"
        )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def deprune(self, ctx, days: int = 30):
        """``deprune [days]`` kicks all pruned members within given date"""
        pruned = await ctx.guild.prune_members(
            days=days, compute_prune_count=True, reason="Inactivity"
        )
        await ctx.send(
            f"`{pruned} have been kicked from the server due to inactivity in the past {days} days!`"
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
    async def quickcategory(
        self, ctx, *, name: commands.clean_content = "Quick Channels"
    ):
        """``quickcategory [category]`` Creates a '+' channel which instantly creates a quick voice channel for the user that joins it"""
        category = await ctx.author.guild.create_category(name)
        await ctx.author.guild.create_voice_channel("\u2795", category=category)
        await ctx.send(
            f"{ctx.author.mention} has setup a `quickcategory` named `{name}`"
        )

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def fullcategory(self, ctx, *, name: commands.clean_content = "No Category"):
        """``fullcategory [category]`` Creates a text channel and a '+' voice channel under a category which instantly creates a quick voice channel for the user that joins it"""
        category = await ctx.author.guild.create_category(name)
        await ctx.author.guild.create_voice_channel("\u2795", category=category)
        await ctx.author.guild.create_text_channel(name, category=category)
        await ctx.send(
            f"{ctx.author.mention} has setup a `fullcategory` named `{name}`"
        )

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def quickchannel(self, ctx, *, name: commands.clean_content = " "):
        """``quickchannel [name]`` Creates a '+' voice channel that creates quick voice channel for the user that joins it"""
        await ctx.author.guild.create_voice_channel(f"\u2795 {name}")
        await ctx.send(
            f"{ctx.author.mention} has setup a `quickchannel` named `\u2795 {name}`"
        )

    @commands.Cog.listener()
    @commands.has_permissions(manage_channels=True)
    async def on_voice_state_update(self, member, before, after):

        if before.channel != after.channel:
            if before.channel is not None:
                if str(before.channel.name) == f"{member.name}'s channel":
                    try:
                        await before.channel.delete()
                    except discord.errors.NotFound:
                        print("Could not delete channel!")

            if after.channel is not None:
                if "\u2795" in str(after.channel.name):
                    channel = await after.channel.clone(name=f"{member.name}'s channel")
                    await member.move_to(channel, reason=None)


def setup(bot):
    bot.add_cog(Mod(bot))

