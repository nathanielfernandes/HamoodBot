import discord
from discord.ext import commands

class Mod(commands.Cog):
    """Server Moderation"""
    def __init__(self, bot):
        self.bot = bot
        # 1 = warning message
        # 2 = automatically deletes the message and shows warning message
        self.profanity_action = 1

    #allows the owner of hamood to temporarily change what actions hamood takes when someone uses profanity
    @commands.command()
    @commands.is_owner()
    async def proflevel(self, ctx, lvl:int):
        """Owner Command"""
        self.profanity_action = lvl

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        """``kick [@user]`` kicks a tagged member"""
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked by {ctx.author.mention}. [{reason}]")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        """``ban [@user]`` bans a tagged member"""
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} was kicked by {ctx.author.mention}. [{reason}]")

    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount=1):
        """``clean`` deletes chat messages"""
        amount = int(amount) + 1
        if amount > 20:
            amount = 20
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=['rename'])
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member = None, *, name: commands.clean_content = None):
        """``nickname [@user] [newname]`` changes the nickname of a member"""
        await member.edit(nick=name) if (name != None) else None


def setup(bot):
    bot.add_cog(Mod(bot))  