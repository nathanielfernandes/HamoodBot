import os
import discord
from discord.ext import commands


import json

blacklist = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/blacklist.json"
    )
)["commandblacklist"][f"{os.path.basename(__file__)[:-3].lower()}"]


class Events(commands.Cog):
    """Handles Any Discord Events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None and member.guild.id not in blacklist:
            await channel.send(f"Welcome {member.mention}!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).embed_links:
                embed = discord.Embed(
                    title=f"Hi {guild}, im Hamood!",
                    description=f"My command prefix is '`.`', use `.help` to get started.\nFor more info use `.info`",
                )
                embed.add_field(
                    name="Server Presence",
                    value=f"Hamood is current in **{len(self.bot.guilds)}** servers\n[Invite Him](https://bit.ly/2XD2YPN)",
                )

                embed.add_field(
                    name="For bugs, further help or suggestions",
                    value="You can message me on discord\n`nathan#3724`",
                )

                # embed.set_footer(
                #     text="created by Nathaniel Fernandes",
                #     icon_url="https://cdn.discordapp.com/attachments/699770186227646465/741388960227655790/k70up0p0ozz21.png",
                # )

                await channel.send(embed=embed)
            break

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{len(bot.guilds)} Servers and {sum([len(g.members) for g in bot.guilds])} Users",
            )
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"`{ctx.command.name} is on cooldown for {str(error.retry_after)[:4]} seconds!`"
            )
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
                    description=f"**{ctx.command.name}** is used like this: `.{s[start:end]}`",
                    colour=discord.Color.red(),
                    timestamp=ctx.message.created_at,
                )
                embed.set_author(
                    name="Error!",
                    icon_url="https://cdn.discordapp.com/attachments/749779629643923548/773072024922095636/images.png",
                )
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                # await ctx.send(
                #     f"{ctx.author.mention}, **{ctx.command.name}** is used like this:\n`.{s[start:end]}`"
                # )
                await ctx.send(embed=embed)
            except Exception:
                print("error")
                # raise error


def setup(bot):
    bot.add_cog(Events(bot))

