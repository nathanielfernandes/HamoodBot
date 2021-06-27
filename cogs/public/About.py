import datetime, time
import discord
from discord.ext import commands
import platform, socket, re, uuid, json, psutil, os

from utils.CONSTANTS import HAMOOD


class About(commands.Cog):
    """About Hamood"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def abouthamood(self, ctx):
        """|||About Hamood."""
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
        # embed.add_field(
        #     name="Source Code",
        #     value="[Click Here](https://github.com/nathanielfernandes/HamoodBot)",
        # )
        embed.add_field(
            name="Command Listing",
            value="Type `.help` or \n[Click Here](https://nathanielfernandes.github.io/HamoodBot/#commands)",
        )
        embed.add_field(
            name="Website",
            value="[**Click Here**](https://hamood.app/)",
        )
        embed.add_field(
            name="For bugs, further help or suggestions",
            value="You can message me on discord\n`nathan#3724`",
        )
        embed.set_thumbnail(
            url=self.bot.user.avatar_url,
        )
        embed.set_footer(
            text="created by Nathaniel Fernandes",
            icon_url="https://cdn.discordapp.com/attachments/699770186227646465/741388960227655790/k70up0p0ozz21.png",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hamoodinfo(self, ctx):
        """|||Information on Hamood."""
        uptime = self.Hamood.pretty_dt(
            (datetime.datetime.now() - self.Hamood.STARTUP).total_seconds()
        )
        process = psutil.Process(os.getpid())
        used = process.memory_info().rss
        total_r = psutil.virtual_memory().total
        ram_used = f"{round(used / (1024.0 ** 3), 3)}GB / {round(total_r / (1024.0 ** 3), 3)}GB"
        total = sum(len(cache) for cache in self.Hamood.Reddit.SubredditCache.values())

        percent = total / 10000
        bar = f"{'█'*round(percent*20)}"
        bar += "░" * (20 - len(bar))
        tic = time.perf_counter()
        await self.Hamood.MONGO.admin.command("ping")
        toc = time.perf_counter()

        embed = discord.Embed(
            description=f"```yaml\n{HAMOOD}```"
            + f"```yaml\n• Uptime: {uptime}\n• Commands Invoked Since Up: {self.Hamood.command_invocations:,}```"
            + f"```yaml\n• Servers: {len(self.bot.guilds):,}\n• Channels: {sum([len(g.channels) for g in self.bot.guilds]):,}\n• Users: {sum([len(g.members) for g in self.bot.guilds]):,}\n• Shards: {self.bot.shard_count}```"
            + f"```yaml\n• Discord Latency: {round(self.bot.latency * 1000):,}ms\n• MongoDB Latency: {round((toc-tic)*1000):,}ms```"
            + f"```yaml\n• Cached Reddit Posts: {total}\n• Capacity: {bar} {round(percent*100, 2)}%```"
            + f"```yaml\n• Images Generated: {self.Hamood.total_gens}\n• Total Size: {self.Hamood.total_gen_bytes/(1024**2):0.2f}MB```"
            + f"```yaml\n• Platform: {platform.system()}\n• Memory: {ram_used}```"
            + f"```yaml\n• Commands: {len(self.bot.commands)}\n• Created On: Tuesday, April 14th, 2020\n• Creator: nathan#3724\n• Library: discord.py v1.7.2```",
            color=discord.Color.teal(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def cogstats(self, ctx):
        stuff = []
        for cog, invokes in self.Hamood.cog_invokes.items():
            percent = invokes / self.Hamood.command_invocations
            bar = f"{'█'*round(percent*20)}"
            bar += "░" * (20 - len(bar))
            bar = bar.zfill(32 - len(cog))
            stuff.append(f"{cog}: {bar.replace('0', ' ')} {round(percent*100, 1)}%")
        stuff = "\n".join(stuff)
        uptime = self.Hamood.pretty_dt(
            (datetime.datetime.now() - self.Hamood.STARTUP).total_seconds()
        )
        await self.Hamood.quick_embed(
            ctx,
            author={"name": "Cog Statistics"},
            description=f"```yaml\nTotal Command Invocations: {self.Hamood.command_invocations}``````yaml\n{stuff}```",
            footer={"text": f"uptime: {uptime}"},
            color=discord.Color.teal(),
        )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def invite(self, ctx):
        """|||Get the invite link for Hamood."""
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
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        """|||Returns the bots latency."""
        await ctx.send(f"Pong! **{round(self.bot.latency * 1000)}ms**")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx, *, query: commands.clean_content = None):
        """[category|command]|||Help for every category and command."""
        p = self.Hamood.find_prefix(ctx.guild.id)

        embed = discord.Embed(color=discord.Color.blurple(), description="", title="")
        embed.set_author(
            name="Hamood Help",
            url="https://hamood.app/",
        )
        # embed.set_footer(
        #     text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        # )

        if query is None:
            embed.description += (
                f"```yaml\nUse {p}help <category> to find out more about it.```"
            )
            categs = []
            for cog_name in self.bot.cogs:
                if self.bot.cogs[cog_name].public:
                    cmnds = self.bot.cogs[cog_name].get_commands()
                    categs.append(f"• `{cog_name}`― {self.bot.cogs[cog_name].__doc__}")
            embed.title = f"Command Categories"
            embed.add_field(name=f"{len(categs)} Categories", value="\n".join(categs))
        else:
            cog_names = {cog.lower(): cog for cog in self.bot.cogs}
            command_names = [c.name for c in self.bot.commands] + [
                y
                for x in [
                    [alias for alias in cmnd.aliases] for cmnd in self.bot.commands
                ]
                for y in x
            ]
            query = query.lower()

            if query in cog_names:
                cog_name = cog_names[query]
                _cog = self.bot.get_cog(cog_name)
                commands = _cog.get_commands()
                embed.description += (
                    f"```yaml\nUse {p}help <command> to find out more about it.```"
                )

                embed.title = f"`{cog_name}` Commands"

                val = [f"`{c.name}`" for c in commands]
                if val:
                    embed.add_field(
                        name=f"{len(commands)} Commands",
                        value=", ".join(val),
                        inline=False,
                    )
            elif query in command_names:
                embed.title = f"`{p}{query}`"

                for command in self.bot.commands:
                    if query == command.name or query in command.aliases:
                        break

                h = command.help.split("|||")
                embed.description += f"{h[1]}\n\n**Usage**\n> `{p}{query} {h[0]}`"
                if len(command.aliases) > 0:
                    aliases = ", ".join(
                        [f"`{c}`" for c in command.aliases] + [f"`{command.name}`"]
                    )
                    embed.description += f"\n\n**Aliases**\n> {aliases}"

                # embed.add_field(name="Usage", value=f"`{p}{query} {h[0]}`")
            else:
                embed.title = "Error"
                embed.description += f"```yaml\nI couldn't find help for that.```\n> `{query}` is not a category or command"

                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/651694663962722304.gif?v=1"
                )

        embed.add_field(
            name="\u200b",
            value="[`Command List`](https://hamood.app/#commands) [`Website`](https://hamood.app/) [`Support Server`](https://discord.gg/MeAz4dpVzK)",
            inline=False,
        )
        await ctx.reply(embed=embed, mention_author=False)

    # @commands.command()
    # @checks.isAllowedCommand()
    # async def vote(self, ctx):
    #     """``vote`` Vote for Hamood to support development and for special rewards."""
    #     await self.Hamood.Inventories.add_member(ctx.guild.id, ctx.author.id)
    #     await self.Hamood.Currency.add_member(ctx.guild.id, ctx.author.id)

    #     embed = discord.Embed(
    #         title="Vote for Hamood",
    #         description="[**Click Here To Vote**](https://top.gg/bot/699510311018823680/vote)",
    #         timestamp=ctx.message.created_at,
    #         color=discord.Color.green(),
    #     )

    #     w = await self.Hamood.dblpy.get_weekend_status()
    #     embed.add_field(
    #         name=f"Rewards {'`x2` Weekend Multiplier' if w else ''}",
    #         value=f"<:blackmarketbox:793618040025645106> Blackmarket Crate `x{1*(2 if w else 1)}`\n<:regularbox:793619180683001876> Regular Crate `x{2*(2 if w else 1)}`\n<:cheque:821591185624793108> Cheque: `x{(2 if w else 1)}`",
    #     )
    #     embed.set_thumbnail(
    #         url="https://cdn.discordapp.com/emojis/778416296630157333.png?v=1"
    #     )
    #     embed.set_footer(text="Double Voting Rewards On Weekends")

    #     await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(About(bot))
