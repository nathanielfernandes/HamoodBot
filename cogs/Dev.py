import discord
from discord.ext import commands


class Dev(commands.Cog):
    """Dev Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        """``logout`` logs hamood out"""
        await ctx.send("**goodbye**")
        await bot.logout()

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, aType: str, uRL: str, *, aName: commands.clean_content):
        """``status [type] [url] [activity]`` lets me change hamoods status"""
        if aType == "playing":
            await self.bot.change_presence(activity=discord.Game(name=aName))
        elif aType == "listening":
            await bot.change_presence(
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
            raise e


def setup(bot):
    bot.add_cog(Dev(bot))
