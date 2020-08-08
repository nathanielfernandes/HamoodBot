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
        else:
            self.running = "?"

    @commands.command()
    async def info(self, ctx):
        """``info`` About Hamood"""
        embed = discord.Embed(title="Hamood", description="Hamood is a Discord bot written with [discord.py](https://github.com/Rapptz/discord.py) that has a variety of helpful and fun functions.", color=discord.Color.blue())
        embed.add_field(name="Background", value="Hamood was created as a fun qurantine project to learn new skills. Hamood's name and profile picture is an inside joke based off the [Yotube](https://knowyourmeme.com/memes/yotube) kid meme.", inline = False)
        embed.add_field(name="Highlighted Features", value="**• Covid-19 Satistics** `New!`\nHamood can send the latest Covid-19 statistics of any country from [worldometer](https://www.worldometers.info/coronavirus/)\n**• Profanity Detection**\nHamood calls out anyone that uses profane words\n**• Custom Text Generated Memes**\nYou can generate custom memes with your own text with the meme templates Hamood has.\n**• Reddit Posts**\nHamood can find and send posts from your favourite subreddits.", inline=False)
        embed.add_field(name="Add him to your server", value=f"Hamood is current in **{len(self.bot.guilds)}** servers.\n[Invite Him](https://bit.ly/2XD2YPN)")
        embed.add_field(name="Source Code", value='[Click Here](https://github.com/nathanielfernandes/HamoodBot)')
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/699510311018823680/bcb476ebfc7c8765a4f673615143996d.webp?size=1024")
        embed.set_footer(text="created by Nathaniel Fernandes", icon_url='https://cdn.discordapp.com/attachments/699770186227646465/741388960227655790/k70up0p0ozz21.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        """``invite`` get the invite link for this bot"""
        embed = discord.Embed(title="Invite Hamood to your server by clicking here!", description="Click the **hyperlink** above to invite Hamood.", color=ctx.author.color, url='https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot')
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/699510311018823680/bcb476ebfc7c8765a4f673615143996d.webp?size=1024")
        embed.add_field(name=f"Hamood is currently in **{len(self.bot.guilds)}** servers", value='make it one more!')
        await ctx.send(embed=embed)


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

        
    #This help command was Written by Jared Newsom (AKA Jared M.F.)!
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
