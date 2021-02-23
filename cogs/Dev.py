import discord
from discord.ext import commands


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
    async def timeout(self, ctx, member: discord.Member = None):
        if member is not None:
            if member.id in self.bot.timeout_list:
                self.bot.timeout_list.remove(member.id)
                await ctx.send(f"**{member}** has been taken out of time out.")
            else:
                self.bot.timeout_list.append(member.id)
                await ctx.send(f"**{member}** has been put in time out.")

    @commands.command()
    @commands.is_owner()
    async def timeout_corner(self, ctx):
        corner = "\n".join(
            [str(self.bot.get_user(id_)) for id_ in self.bot.timeout_list]
        )
        await ctx.send(f"```{corner}```")


def setup(bot):
    bot.add_cog(Dev(bot))
