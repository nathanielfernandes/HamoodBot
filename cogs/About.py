import datetime
import platform
import discord
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.VERSION = "Hamood v12.6" 
        self.currentDT = str(datetime.datetime.now())

        if (platform.system() == 'Darwin'):
            self.running = 'macOS Catalina'
        elif (platform.system() == 'Linux'):
            self.running = 'Heroku Linux'

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        """get the invite link for this bot"""
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot')

    @commands.command(aliases=['repo'])
    async def github(self, ctx):
        """sends the link to Hamood's github repository"""
        await ctx.send('https://github.com/nathanielfernandes/HamoodBot')

    @commands.command()
    async def version(self, ctx):
        """sends Hamood's current version"""
        self.currentDT = datetime.datetime.now()
        await ctx.send(f'```md\n[{self.VERSION} | {self.currentDT}](RUNNING ON: {self.running})```')

    @commands.command()
    async def ping(self, ctx):
        """returns hamood's ping"""
        await ctx.send(f"```xl\n'pong! {self.bot.latency}```")


def setup(bot):
    bot.add_cog(About(bot))