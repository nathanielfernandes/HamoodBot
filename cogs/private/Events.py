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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        p = self.Hamood.find_prefix(ctx.guild.id)
        timeout = False
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title=f"`{ctx.command.name}` is on cooldown for",
                description=f"```{self.Hamood.pretty_time_delta(error.retry_after)}```",
                colour=discord.Color.red(),
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

            timeout = True
        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("`You don't have the permission to do that`")

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == "tag list":
                await ctx.send("`I could not find that member`")

        elif isinstance(error, commands.CommandError):
            try:
                s = ctx.command.help
                start = s.find("``") + 2
                end = s.find("``", start)

                embed = discord.Embed(
                    title="Command Failed",
                    description=f"**{ctx.command.name}** is used like this: ```ini\n{p}{s[start:end]}```",
                    colour=discord.Color.red(),
                    timestamp=ctx.message.created_at,
                )
                # embed.set_author(
                #     name="Error!",
                #     icon_url="https://cdn.discordapp.com/attachments/749779629643923548/773072024922095636/images.png",
                # )
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/749779300181606411/799902760837316628/tumblr_01a3fd42036dbeac4d74baff3a2497ff_ecd049b3_500.gif"
                )
                # await ctx.send(
                #     f"{ctx.author.mention}, **{ctx.command.name}** is used like this:\n`.{s[start:end]}`"
                # )
                await ctx.send(embed=embed)
            except Exception:
                print("error")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("`I don't have the permission to do that`")
        else:
            await ctx.send("`Error`")

        if not timeout:
            ctx.command.reset_cooldown(ctx)


def setup(bot):
    bot.add_cog(Events(bot))

