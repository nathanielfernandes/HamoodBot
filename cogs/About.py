import datetime
import platform
import discord
from discord.ext import commands

class About(commands.Cog):
    """About Hamood"""
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
        """``invite`` get the invite link for this bot"""
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot')

    @commands.command(aliases=['repo'])
    async def github(self, ctx):
        """``github`` sends the link to Hamood's github repository"""
        await ctx.send('https://github.com/nathanielfernandes/HamoodBot')

    @commands.command()
    async def version(self, ctx):
        """``version`` sends Hamood's current version"""
        self.currentDT = datetime.datetime.now()
        await ctx.send(f'```md\n[{self.VERSION} | {self.currentDT}](RUNNING ON: {self.running})```')

    @commands.command()
    async def ping(self, ctx):
        """``ping`` returns hamood's ping"""
        await ctx.send(f"```xl\n'pong! {self.bot.latency}```")

        
    #This help command was Written by Jared Newsom (AKA Jared M.F.)!#
    #https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b
    @commands.command()
    async def help(self,ctx,*cog):
        """Gets all cogs and commands of Hamood"""
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title='Command Categories', description='Use `help <category>` to find out more about them!\nIf you want to know how to use a specific command\njust send it alone and I will help.')
                halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.send('',embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many categories!',color=discord.Color.red())
                    halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send('',embed=halp)
                else:
                    """Command listing within a Category."""
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
                                halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                found = True
                    if not found:
                        """Reminds you if that category doesn't exist."""
                        halp = discord.Embed(title='Error!',description=f'How do you even use {cog[0]}',color=discord.Color.red())
                        halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send('',embed=halp)
        except:
            await ctx.send("Excuse me, I can't send embeds.")

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(About(bot))
