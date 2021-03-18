import discord
from discord.ext import commands
import asyncio


class Dev(commands.Cog):
    """Dev Commands"""

    def __init__(self, bot):
        self.bot = bot

    def to_id(self, name):
        return name.replace(" ", "_").lower()

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        """``logout`` logs hamood out"""
        await ctx.send("**goodbye**")
        await self.bot.aioSession.close()
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, aType: str, uRL: str, *, aName: commands.clean_content):
        """``status [type] [url] [activity]`` lets me change hamoods status"""
        if aType == "playing":
            await self.bot.change_presence(activity=discord.Game(name=aName))
        elif aType == "listening":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, name=aName
                )
            )
        elif aType == "watching":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=aName
                )
            )
        elif aType == "streaming":
            await self.bot.change_presence(
                activity=discord.Streaming(name=aName, url=uRL)
            )

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """``reload [cog name]`` reloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got reloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """``unload [cog name]`` unloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got unloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be unloaded:`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        """``load [cog name]`` loads the requested cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got loaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded:`")
            raise

    @commands.command()
    @commands.is_owner()
    async def gameslog(self, ctx):
        log = "\n".join([f"{self.bot.games_log[k]} | {k}" for k in self.bot.games_log])
        await ctx.send(f"```{len(self.bot.games_log)} Games:\n{log}```")

    @commands.command()
    @commands.is_owner()
    async def get_item(self, ctx, item_id, amount=1):
        """``get_item [item_id] [amount]`` get any item"""
        amount = int(amount)
        await self.bot.inventories.add_inventory(ctx.guild.id)
        await self.bot.inventories.add_member(ctx.guild.id, ctx.author.id)
        await self.bot.inventories.add_item(
            ctx.guild.id, ctx.author.id, self.to_id(item_id), int(amount)
        )
        await ctx.send(f"`You recieved {item_id} x{amount}`")

    @commands.command()
    @commands.is_owner()
    async def print_money(self, ctx, amount):
        """``print_money [amount]`` get any amount of money"""
        await self.bot.currency.add_server(ctx.guild.id)
        await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)
        await self.bot.currency.update_wallet(ctx.guild.id, ctx.author.id, int(amount))

        await ctx.send(f"`You recieved ⌬ {int(amount):,}`")

    @commands.command()
    @commands.is_owner()
    async def wipe(self, ctx, member: discord.Member = None):
        if member is not None:
            # await self.bot.leaderboards.delete_member(member.guild.id, member.id)
            await self.bot.currency.delete_member(member.guild.id, member.id)
            await self.bot.inventories.delete_member(member.guild.id, member.id)

            await ctx.send(f"{member.mention} has been wiped from the db")

    @commands.command()
    @commands.is_owner()
    async def silence(self, ctx, member: discord.Member = None, hours=None):
        if member is not None:
            if member.id in self.bot.timeout_list:
                self.bot.timeout_list.remove(member.id)
                await ctx.send(f"**{member}** has been taken out of time out.")
            else:
                self.bot.timeout_list.append(member.id)
                if hours is None:
                    await ctx.send(
                        f"**{member}** has been put in time out. `Indefinitely`"
                    )
                else:
                    time = 3600 * hours
                    await ctx.send(
                        f"**{member}** has been put in time out for {self.bot.pretty_time_delta(time)}"
                    )
                    await asyncio.sleep(time)
                    self.bot.timeout_list.remove(member.id)

    @commands.command()
    @commands.is_owner()
    async def inspect(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        content = await ctx.send(
            f"`Gathering information on {member}...` <a:load:822030219924733992>"
        )
        await asyncio.sleep(3)

        msg = f"```ini\n[username]: {member}"
        msg += f"\n[id]: {member.id}"
        msg += f"\n[created at]: {member.created_at}"
        msg += f"\n[is bot?]: {member.bot}"
        msg += f"\n[in timeout?]: {member.id in self.bot.timeout_list}\n"

        servers, bal = await self.bot.currency.find_all_of_member(member.id)
        total = await self.bot.inventories.find_all_of_member(member.id)
        won, lost = await self.bot.leaderboards.find_all_of_member(member.id)
        servers = [self.bot.get_guild(int(g)) for g in servers]
        servers = "\n - ".join(
            [f"{g.name} ({g.member_count} users)" for g in servers if g is not None]
        )
        msg += f"\n[known servers]:\n - {servers}\n"
        try:
            ready, time, streak = await self.bot.members.is_daily_ready(member.id)
            msg += f"\n[daily]:\n - ready?: {ready}\n - timeleft: {time:0.0f}s\n - streak: {streak}\n"
        except:
            pass

        msg += f"\n[total balance (across {bal['total']} servers)]:\n - wallet: ⌬ {bal['wallet']:,}\n - bank: ⌬ {bal['bank']:,}\n"
        msg += f"\n[total items (across {bal['total']} servers)]:\n - {total:,}\n"
        msg += f"\n[total leaderboard (across {bal['total']} servers)]:\n - won: {won:,}\n - lost: {lost:,}\n"
        msg += "```"

        embed = discord.Embed(
            title=f"User Details (Hamood) - {member.display_name}",
            colour=member.color,
            timestamp=ctx.message.created_at,
            description=msg,
        )

        embed.set_thumbnail(url=member.avatar_url)
        await content.edit(embed=embed, content=None)

    @commands.command()
    @commands.is_owner()
    async def timeout_corner(self, ctx):
        corner = "\n".join(
            [str(self.bot.get_user(id_)) for id_ in self.bot.timeout_list]
        )
        await ctx.send(f"```{corner}```")


def setup(bot):
    bot.add_cog(Dev(bot))
