import dbl
import datetime
import discord
from discord.ext import commands

import modules.checks as checks

import platform, socket, re, uuid, json, psutil, os

try:
    TOKEN = os.environ["TOKEN"]
    TOPGG = os.environ["TOPGG"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.environ.get("BOTTOKENTEST")
    TOPGG = os.environ.get("TOPGG")


class About(commands.Cog):
    """About Hamood"""

    def __init__(self, bot):
        self.bot = bot
        self.currentDT = str(datetime.datetime.now())
        self.start = datetime.datetime.now()
        self.dblpy = dbl.DBLClient(
            self.bot, TOPGG,
        )  # Autopost will post your guild count every

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
        # embed.add_field(
        #     name="Highlighted Features",
        #     value="**• Filler Game** `New!`\nYou can now play the popular imsg game 'Filler' with hamood.\n**• Complex Math**\nHamood has new and improved math functions that can help you with your homework.\n**• Custom Text Generated Memes**\nYou can generate custom memes with your own text with the meme templates Hamood has.\n**• Reddit Posts**\nHamood can find and send posts from your favourite subreddits.\n**• Profanity Detection**\nHamood flags any message with a bad word\n",
        #     inline=False,
        # )
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
            name="Website",
            value="[**Click Here**](https://nathanielfernandes.github.io/HamoodBot/)",
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
        general = self.bot.get_cog("General")
        uptime = general.pretty_time_delta(
            (datetime.datetime.now() - self.start).total_seconds()
        )

        ram_used = f"{round(psutil.virtual_memory().used / (1024.0 ** 3), 2)}GB / {round(psutil.virtual_memory().total / (1024.0 ** 3), 2)}GB"

        embed = discord.Embed(
            title="<:hamood:713523447141236867> Hamood Info",
            description=f"```py\nUptime: {uptime}```",
            color=discord.Color.teal(),
        )
        # embed.add_field(name="Uptime", value=f"```py\n{uptime}```", inline=True)
        embed.add_field(
            name="Discord Presence",
            value=f"```py\nGuilds: {len(self.bot.guilds):,}\nChannels: {sum([len(g.channels) for g in self.bot.guilds]):,}\nUsers: {sum([len(g.members) for g in self.bot.guilds]):,}\nShards: {self.bot.shard_count}```",
            inline=False,
        )
        embed.add_field(
            name="System",
            value=f"```py\nLatency: {round(self.bot.latency * 1000)}ms\nPlatform: {platform.system()}```",
            inline=False,
        )

        # embed.add_field(
        #     name="Basic Info",
        #     value=f"```py\nCommands: {len(self.bot.commands)}\nLibrary: discord.py v 1.5.1\nCreated On: Tue, April 14th, 2020\nCreated By: 'nathan#3724'```",
        #     inline=False,
        # )

        embed.set_image(url="https://top.gg/api/widget/699510311018823680.png")

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
        await self.bot.inventories.add_member(ctx.guild.id, ctx.author.id)
        await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)

        embed = discord.Embed(
            title="Vote for Hamood",
            description="[**Click Here To Vote**](https://top.gg/bot/699510311018823680/vote)",
            timestamp=ctx.message.created_at,
            color=discord.Color.green(),
        )

        w = await self.dblpy.get_weekend_status()
        # <:blackmarketbox:793618040025645106> Blackmarket Crate `x{1*(2 if w else 1)}`\n
        embed.add_field(
            name=f"Rewards {'`x2` Weekend Multiplier' if w else ''}",
            value=f"<:regularbox:793619180683001876> Regular Crate `x{2*(2 if w else 1)}`\n<a:coin:790679388147679272> Money: [⌬ {2500*(2 if w else 1):,}](https://top.gg/bot/699510311018823680)",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/778416296630157333.png?v=1"
        )
        embed.set_footer(text="Double Voting Rewards On Weekends")

        await ctx.send(embed=embed)

    # @commands.command()
    # async def version(self, ctx):
    #     """``version`` sends Hamood's current version"""
    #     self.currentDT = datetime.datetime.now()
    #     await ctx.send(
    #         f"```md\n[{self.VERSION} | {self.currentDT}](RUNNING ON: {self.running})```"
    #     )

    @commands.command()
    @checks.isAllowedCommand()
    async def ping(self, ctx):
        await ctx.send(f"Pong! **{round(self.bot.latency * 1000)}ms**")

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def help(self, ctx, query=None):
        """``help [category or command]``"""
        if query is None:
            halp = discord.Embed(
                title="Command Categories",
                description="Use `.help [category]` to find out more about them!\nYou can also just click [**here**](https://nathanielfernandes.github.io/HamoodBot/#commands) for info on all the commands.",
                color=discord.Color.blue(),
            )
            cogs_desc = ""
            for cog in self.bot.cogs:
                if cog not in ["Events", "TopGG", "Dev", "Web"]:
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
            if query.capitalize() in self.bot.cogs:
                for cog in self.bot.cogs:
                    if query.lower() == str(cog).lower():
                        halp = discord.Embed(
                            title=f"{cog} Command Listing",
                            description=f"{self.bot.cogs[str(cog)].__doc__}\n Use `.help [command]` to find out how to use a specific command.",
                            color=discord.Color.blue(),
                        )

                        commands = self.bot.get_cog(cog).get_commands()
                        val = [f"`{c.name}`" for c in commands]
                        halp.add_field(
                            name=f"{len(commands)} Commands", value=", ".join(val)
                        )
            elif query.lower() in command_names:
                for command in self.bot.commands:
                    if query.lower() == command.name:
                        halp = discord.Embed(
                            title=f"`{command.name.capitalize()}` Command Help",
                            description=f"**.**{command.help}",
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
