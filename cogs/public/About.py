import datetime, time
import discord
from discord.ext import commands

import modules.checks as checks

import platform, socket, re, uuid, json, psutil, os


class About(commands.Cog):
    """About Hamood"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(embed_links=True)
    async def abouthamood(self, ctx):
        """``abouthamood`` About Hamood"""
        embed = discord.Embed(
            title="Hamood",
            description="Hamood is a Discord bot written with [discord.py](https://github.com/Rapptz/discord.py) that has a variety of helpful and fun functions.",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Background",
            value="Hamood was created as a fun qurantine project to learn new skills. Hamood's name and profile picture is an inside joke based off the [Yotube](https://knowyourmeme.com/memes/yotube) kid meme.",
            inline=False,
        )

        embed.add_field(
            name="Server Presence",
            value=f"Hamood is current in **{len(self.bot.guilds)}** servers\n[Invite Him](https://bit.ly/2XD2YPN)",
        )
        embed.add_field(
            name="Source Code",
            value="[Click Here](https://github.com/nathanielfernandes/HamoodBot)",
        )

        embed.add_field(
            name="Command Listing",
            value="Type `.help` or \n[Click Here](https://nathanielfernandes.github.io/HamoodBot/#commands)",
        )

        embed.add_field(
            name="Website", value="[**Click Here**](https://hamood.app/)",
        )

        embed.add_field(
            name="For bugs, further help or suggestions",
            value="You can message me on discord\n`nathan#3724`",
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url,)
        embed.set_footer(
            text="created by Nathaniel Fernandes",
            icon_url="https://cdn.discordapp.com/attachments/699770186227646465/741388960227655790/k70up0p0ozz21.png",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    async def info(self, ctx):
        """``info`` info on Hamood"""

        uptime = self.Hamood.pretty_time_delta(
            (datetime.datetime.now() - self.Hamood.STARTUP).total_seconds()
        )

        # ram_used = f"{round(psutil.virtual_memory().used / (1024.0 ** 3), 2)}GB / {round(psutil.virtual_memory().total / (1024.0 ** 3), 2)}GB"

        embed = discord.Embed(
            title="Hamood Info",
            description=f"```py\nUptime: {uptime}```",
            color=discord.Color.teal(),
        )
        embed.add_field(
            name="Discord Presence",
            value=f"```py\nServers: {len(self.bot.guilds):,}\nChannels: {sum([len(g.channels) for g in self.bot.guilds]):,}\nUsers: {sum([len(g.members) for g in self.bot.guilds]):,}\nShards: {self.bot.shard_count}```",
            inline=False,
        )
        embed.add_field(
            name="System",
            value=f"```py\nLatency: {round(self.bot.latency * 1000)}ms\nPlatform: {platform.system()}```",
            inline=False,
        )

        embed.add_field(
            name="Basic Info",
            value=f"```py\nCommands: {len(self.bot.commands)}\nLibrary: discord.py v 1.5.1\nCreated On: Tue, April 14th, 2020\nCreated By: 'nathan#3724'```",
            inline=False,
        )

        embed.set_image(
            url=f"https://top.gg/api/widget/699510311018823680.png?hamood={str(time.time())[-6:]}"
        )

        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url,
        )
        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    async def invite(self, ctx):
        """``invite`` get the invite link for Hamood"""
        embed = discord.Embed(
            title="Invite Hamood to your server by clicking here!",
            description="Click the **hyperlink** above to invite Hamood.",
            color=discord.Color.blue(),
            url="https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot",
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name=f"Hamood is currently in **{len(self.bot.guilds)}** servers",
            value="make it one more!",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    async def vote(self, ctx):
        """``vote`` Vote for Hamood to support development and for special rewards."""
        await self.Hamood.Inventories.add_member(ctx.guild.id, ctx.author.id)
        await self.Hamood.Currency.add_member(ctx.guild.id, ctx.author.id)

        embed = discord.Embed(
            title="Vote for Hamood",
            description="[**Click Here To Vote**](https://top.gg/bot/699510311018823680/vote)",
            timestamp=ctx.message.created_at,
            color=discord.Color.green(),
        )

        w = await self.Hamood.dblpy.get_weekend_status()
        embed.add_field(
            name=f"Rewards {'`x2` Weekend Multiplier' if w else ''}",
            value=f"<:blackmarketbox:793618040025645106> Blackmarket Crate `x{1*(2 if w else 1)}`\n<:regularbox:793619180683001876> Regular Crate `x{2*(2 if w else 1)}`\n<:cheque:821591185624793108> Cheque: `x{(2 if w else 1)}`",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/778416296630157333.png?v=1"
        )
        embed.set_footer(text="Double Voting Rewards On Weekends")

        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    async def ping(self, ctx):
        await ctx.send(f"Pong! **{round(self.bot.latency * 1000)}ms**")

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def help(self, ctx, query=None):
        """``help [category or command]``"""
        p = self.Hamood.find_prefix(ctx.guild.id)
        if query is None:
            halp = discord.Embed(
                title="Command Categories",
                description=f"Use `{p}help [category]` to find out more about them!\nYou can also just click [**here**](https://hamood.app/#commands) for info on all the commands. [Support Server](https://discord.gg/7dEuxNq3)",
                color=discord.Color.blue(),
            )
            cogs_desc = ""
            for cog in self.bot.cogs:
                if cog not in ["Events", "TopGG", "Dev", "Web", "Cps310"]:
                    cogs_desc += f"`{cog}` - {self.bot.cogs[cog].__doc__}\n"

            halp.add_field(
                name="Categories",
                value=cogs_desc[0 : len(cogs_desc) - 1],
                inline=False,
            )
            cmds_desc = ""
            for cmnd in self.bot.walk_commands():
                if not cmnd.cog_name and not cmnd.hidden:
                    cmds_desc += f"`{cmnd.name}` - {cmnd.help}\n"
            # halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
        else:
            command_names = [c.name for c in self.bot.commands]
            for i in self.bot.commands:
                for j in i.aliases:
                    command_names.append(j)

            if query.capitalize() in self.bot.cogs:
                for cog in self.bot.cogs:
                    if query.lower() == str(cog).lower():
                        halp = discord.Embed(
                            title=f"{cog} Command Listing",
                            description=f"{self.bot.cogs[str(cog)].__doc__}\n Use `{p}help [command]` to find out how to use a specific command.",
                            color=discord.Color.blue(),
                        )

                        commands = self.bot.get_cog(cog).get_commands()
                        val = [f"`{c.name}`" for c in commands]
                        halp.add_field(
                            name=f"{len(commands)} Commands", value=", ".join(val)
                        )
            elif query.lower() in command_names:
                for command in self.bot.commands:
                    if (
                        query.lower() == command.name
                        or query.lower() in command.aliases
                    ):
                        if len(command.aliases) > 0:
                            a = "\n\nAliases: " + ", ".join(
                                ["`" + i + "`" for i in command.aliases]
                            )
                        else:
                            a = ""
                        halp = discord.Embed(
                            title=f"`{command.name.capitalize()}` Command Help",
                            description=f"**{p}**{command.help}{a}",
                            color=discord.Color.blue(),
                        )
            else:
                halp = discord.Embed(
                    title="Error!",
                    description=f"I couldn't find help for that.\n`{query}` is not a **category** or **command**",
                    color=discord.Color.red(),
                )
                halp.set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/651694663962722304.gif?v=1"
                )

        halp.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )
        await ctx.send("", embed=halp)


def setup(bot):
    bot.add_cog(About(bot))
