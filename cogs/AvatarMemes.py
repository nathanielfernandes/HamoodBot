import os
import sys
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import image_functions
import web_scraping

class AvatarMemes(commands.Cog):
    """Custom Avatar Memes"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def stonks(self, ctx, *avamember : discord.Member):
        """``stonks [@user]`` adds a tagged discord avatar to the 'stonks' meme"""
        await imagePrep(ctx, avamember, [[(65, 20), 0]], "stonksImage.jpg", (200,200))

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def worthless(self, ctx, *avamember : discord.Member):
        """``worthless [@user]`` adds a tagged discord avatar to the 'this is worthless' meme"""
        await imagePrep(ctx, avamember, [[(490, 235), -10]], "worthlessImage.jpg", (450,450))
            
    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def neat(self, ctx, *avamember : discord.Member):
        """``neat [@user]`` adds a tagged discord avatar to the 'this is pretty neat' meme"""
        await imagePrep(ctx, avamember, [[(16, 210), 0]], "neatImage.jpg", (270,270))

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def grab(self, ctx, *avamember : discord.Member):
        """``grab [@user]`` adds a tagged discord avatar to the 'grab' meme"""
        await imagePrep(ctx, avamember, [[(25, 265), 0]], "grabImage.jpg", (150,150))



async def imagePrep(ctx, member, stuff, memeImage, size):
    path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1]

    async with ctx.typing():
        member = list(member)
        member.append(ctx.author)
        
        Urls = []
        for a in member:
            userAvatarUrl = str(a.avatar_url)
            userAvatarUrl = userAvatarUrl.replace('.webp', '.png')
            Urls.append(userAvatarUrl)

        for i in range(len(stuff)):
            stuff[i].append(Urls[i])
        
        for item in stuff:
            name = image_functions.randomNumber()
            name = str(name) + '.png'
            save = path + '/' + "tempImages" '/' + name
            web_scraping.scrape(item[2], save)
            
            pos = stuff.index(item)
            stuff[pos][2] = save

        finalName = image_functions.randomNumber()
        finalName = str(finalName) + '.jpg'

        meme = image_functions.addImage(memeImage, stuff, size, finalName)
        
        for item in stuff:
            os.remove(item[2])
        
        #await ctx.message.delete()
        try:
            await ctx.send(file=discord.File(meme))
        except discord.Forbidden:
            print('could not send!')

    os.remove(meme)


def setup(bot):
    bot.add_cog(AvatarMemes(bot))  