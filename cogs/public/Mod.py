import discord
from discord.ext import commands
from collections import Counter


class Offender(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages
        if not permission:
            return argument
        else:
            raise commands.BadArgument("Cannot affect members higher than mod.")


class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted in argument.roles:
            return argument
        else:
            raise commands.BadArgument("The user was not muted.")


class Mod(commands.Cog):
    """Server Moderation Commands. Works best when the bot's role is the heighest."""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    async def muteII(self, ctx, user, reason):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            try:
                muted = await ctx.guild.create_role(
                    name="Muted", reason="To use for muting"
                )
                for channel in ctx.guild.channels:
                    await channel.set_permissions(
                        muted,
                        send_messages=False,
                    )
            except discord.Forbidden:
                return await self.Hamood.quick_embed(
                    ctx, title="I don't have the permissions to make a muted role!"
                )
            await user.add_roles(muted)
        else:
            await user.add_roles(role)

    async def do_removal(self, ctx, limit, predicate, *, before=None, after=None):
        if limit > 2000:
            return await self.Hamood.quick_embed(
                ctx, description=f"Too many messages to search given ({limit}/2000)"
            )
        if before is None:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after is not None:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(
                limit=limit, before=before, after=after, check=predicate
            )
        except discord.Forbidden:
            return await self.Hamood.quick_embed(
                ctx, description=f"I dont have the permissions to delete messages."
            )
        except discord.HTTPException:
            return await self.Hamood.quick_embed(
                ctx,
                description=f"Could not delete messages. Try lowering the search amount.",
            )

        spammers = Counter(m.author.display_name for m in deleted)
        deleted = len(deleted)
        messages = [
            f'\n{deleted} message{" was" if deleted == 1 else "s were"} removed.'
        ]
        if deleted:
            messages.append("")
            spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
            messages.extend(f"{name}: {count}" for name, count in spammers)

        to_send = "\n".join(messages)

        if len(to_send) > 2000:
            await self.Hamood.quick_embed(
                ctx, description=f"Successfully removed {deleted} messages."
            )
        else:
            await self.Hamood.quick_embed(ctx, description=f"{to_send}")

    @commands.command(aliases=["clean", "purge"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, search: int = 10, member: discord.Member = None):
        """<search amount> [@member]|||Mass clears messages from the chat."""
        if member is not None:
            check = lambda e: e.author == member
        else:
            check = lambda e: True

        await self.do_removal(ctx, search, check, before=ctx.message.id)

    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(
        embed_links=True, manage_channels=True, manage_roles=True
    )
    @commands.cooldown(5, 20, commands.BucketType.guild)
    async def mute(self, ctx, user: Offender, reason=None):
        """<@member> [reason]|||Mutes a member in the server preventing them from sending messages in any channels."""
        await self.muteII(ctx, user, reason or "No Reason")
        await self.Hamood.quick_embed(
            ctx,
            description=f"{user.mention} has been muted\nReason: `{reason or 'No Reason'}`",
        )

    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(
        embed_links=True, manage_channels=True, manage_roles=True
    )
    @commands.cooldown(5, 20, commands.BucketType.guild)
    async def unmute(self, ctx, user: Redeemed):
        """<@member>|||Unmutes a muted member."""
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await self.Hamood.quick_embed(
            ctx,
            description=f"{user.mention} has been unmuted.",
        )

    @commands.command()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True, embed_links=True)
    @commands.cooldown(10, 20, commands.BucketType.guild)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        """<@member> [reason]|||Kicks a member from the server."""
        await member.kick(reason=reason)
        await self.Hamood.quick_embed(
            ctx,
            description=f"{member.mention} was `kicked` by {ctx.author.mention}\nReason: `{reason}`",
        )

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True, embed_links=True)
    @commands.cooldown(10, 20, commands.BucketType.guild)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        """<@member>|||Bans a member from the server."""
        await member.ban(reason=reason)
        await self.Hamood.quick_embed(
            ctx,
            description=f"{member.mention} was `banned` by {ctx.author.mention}\nReason: `{reason}`",
        )

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(10, 20, commands.BucketType.guild)
    async def softban(self, ctx, member: discord.Member, *, reason="No reason"):
        """<@member>|||Softbans a member from the server."""
        await member.ban(reason=reason)
        await member.unban()
        await self.Hamood.quick_embed(
            ctx,
            description=f"{member.mention} was `softbanned` by {ctx.author.mention}\nReason: `{reason}`",
        )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True, embed_links=True)
    @commands.cooldown(2, 5, commands.BucketType.guild)
    async def prunes(self, ctx, days: int = 7):
        """[days]|||Returns how many roleless members have not been active on the server."""
        prunes = await ctx.guild.estimate_pruned_members(days=days)
        await self.Hamood.quick_embed(
            ctx,
            description=f"`{prunes}` roleless members have not been active for `{days}` days.",
        )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True, embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def deprune(self, ctx, days: int = 30):
        """[days]|||Kicks all roleless members that have not been active on the server."""
        pruned = await ctx.guild.prune_members(
            days=days, compute_prune_count=True, reason="Inactivity"
        )
        await self.Hamood.quick_embed(
            ctx,
            description=f"`{pruned}` have been kicked from the server due to inactivity in the past `{days}` days!",
        )


def setup(bot):
    bot.add_cog(Mod(bot))
