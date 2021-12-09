import random, json, datetime
import discord
from discord.ext import commands


class User(commands.Cog):
    """Get Users Information"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def joined(self, ctx, member: discord.Member = None):
        """[@mention]|||Findout when a member joined the server."""
        member = ctx.author if not member else member
        await self.Hamood.quick_embed(
            ctx,
            author={"name": str(member), "icon_url": member.avatar.url},
            description=f'Joined **{ctx.guild.name}** on:```yaml\n{member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC")}```\n**Total time here**:\n{self.Hamood.pretty_dt((datetime.datetime.now() - member.joined_at).total_seconds())}',
        )

    @commands.command(aliases=["avatar"])
    @commands.bot_has_permissions(embed_links=True)
    async def pfp(self, ctx, member: discord.Member = None):
        """[@mention]|||Get the profile picture of user."""
        member = ctx.author if not member else member
        await self.Hamood.quick_embed(
            ctx,
            author={"name": f"{member}'s avatar", "url": member.avatar.url},
            image_url=member.avatar.url,
        )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def roles(self, ctx, member: discord.Member = None):
        """[@mention]|||Lists the roles of a user."""
        member = ctx.author if not member else member
        roles = [role.mention for role in member.roles]
        await self.Hamood.quick_embed(
            ctx,
            author={"name": f"{member}'s roles"},
            thumbnail=member.avatar.url,
            fields=[
                {
                    "name": "Top Role",
                    "value": member.top_role.mention,
                    "inline": "False",
                },
                {"name": f"All Roles ({len(roles)})", "value": " ".join(roles)},
            ],
        )

    @commands.command(aliases=["perms"])
    @commands.bot_has_permissions(embed_links=True)
    async def permissions(self, ctx, member: discord.Member = None):
        """[@mention]|||Get a list of a users permissions in the server."""
        member = ctx.author if not member else member
        perms = "\n".join(
            f"• {str(perm[0]).replace('_', ' ').capitalize()}"
            for perm in member.guild_permissions
            if perm[1]
        )

        await self.Hamood.quick_embed(
            ctx,
            author={"name": f"{member}'s permissions", "icon_url": member.avatar.url},
            description=perms,
        )

    @commands.command(aliases=["ui"])
    @commands.bot_has_permissions(embed_links=True)
    async def userinfo(self, ctx, member: discord.Member = None):
        """[@mention]|||Findout allot of information on a user."""
        member = ctx.author if not member else member
        roles = [role.mention for role in member.roles]
        perms = [
            f"`{str(perm[0]).replace('_', ' ').capitalize()}`"
            for perm in member.guild_permissions
            if perm[1]
        ]
        if "`Administrator`" in perms:
            perms = ["`Adminstrator`"]

        await self.Hamood.quick_embed(
            ctx,
            author={"name": f"User Info - {member}"},
            description=f"**Nick Name:** {member.display_name}\n**ID:** {member.id}\n**Is Bot:** {member.bot}\n**Vibe:** {random.choice(self.Hamood.RANDOMWORDS)} {random.choice(self.Hamood.RANDOMEMOJIS)}\u200b",
            thumbnail=member.avatar.url,
            fields=[
                {
                    "name": "Top Role",
                    "value": member.top_role.mention,
                    "inline": False,
                },
                {
                    "name": f"All Roles ({len(roles)})",
                    "value": " ".join(roles),
                    "inline": False,
                },
                {
                    "name": "Joined Discord",
                    "value": f'{member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")}\n*{self.Hamood.pretty_dt((datetime.datetime.now() - member.created_at).total_seconds())} ago*',
                    "inline": False,
                },
                {
                    "name": "Joined Server",
                    "value": f'{member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC")}\n*{self.Hamood.pretty_dt((datetime.datetime.now() - member.joined_at).total_seconds())} ago*',
                    "inline": False,
                },
                {
                    "name": f"Permissions ({len(perms)})",
                    "value": ", ".join(perms),
                    "inline": False,
                },
            ],
        )


def setup(bot):
    bot.add_cog(User(bot))
