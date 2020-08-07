import os
import sys
import discord
import textwrap
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import image_functions

class Text_Memes(commands.Cog):
    """Custom Text Generation Memes"""
    def __init__(self, bot):
        self.bot = bot
    
    
    async def textMemePrep(self, ctx, text, coords, font, colour, source, wrap=12):
        async with ctx.typing():

            text = text.split(', ')

            for i in range(len(text)):
                text[i] = textwrap.wrap(text[i], width=wrap)
                for a in range(len(text[i])):
                    text[i][a] += '\n'
                text[i] = ' '.join(text[i])

            for i in range(len(coords)):
                coords[i].append(text[i])
            
            name = image_functions.randomNumber()
            name = str(name) + '.jpg'

            meme = image_functions.addText(source, font, colour, coords, name)
            #await ctx.message.delete()
            await ctx.send(file=discord.File(meme))
        os.remove(meme)


    @commands.command()
    async def bonk(self, ctx, *, content: commands.clean_content):
        """``bonk [text1], [text2]`` adds your own text to the 'bonk' meme format"""
        await self.textMemePrep(ctx, content, [[(250,450)],[(1050,600)]], 75, 'BLACK', 'bonkImage.jpg')

    @commands.command()
    async def lick(self, ctx, *, content: commands.clean_content):
        """``lick [text1], [text2]`` adds your own text to the 'lick' meme format"""
        await self.textMemePrep(ctx, content, [[(320,220)],[(75,200)]], 35, 'BLACK', 'lickImage.jpg')

    @commands.command()
    async def slap(self, ctx, *, content: commands.clean_content):
        """``slap [text1], [text2]`` adds your own text to the 'slap' meme format"""
        await self.textMemePrep(ctx, content, [[(580, 30)],[(220, 250)]], 60, 'WHITE', 'slapImage.jpg')

    @commands.command()
    async def lookback(self, ctx, *, content: commands.clean_content):
        """``lookback [text1], [text2], [text3]`` adds your own text to the 'lookback' meme format"""
        await self.textMemePrep(ctx, content, [[(120, 285)],[(360, 180)],[(525, 250)]], 30, 'BLACK', 'lookBackImage.jpg', 14)

    @commands.command()
    async def our(self, ctx, *, content: commands.clean_content):
        """``our [text1], [text2]`` adds your own text to the 'our' meme format"""
        content = 'our ' + content + ',  '
        await self.textMemePrep(ctx, content, [[(325,320)], [(310,110)]], 45, 'BLACK', 'sovietImage.jpg')

    @commands.command()
    async def pour(self, ctx, *, content: commands.clean_content):
        """``pour [text1], [text2]``adds your own text to the 'pour' meme format"""
        await self.textMemePrep(ctx, content, [[(50,110)], [(430,60)]], 45, 'BLACK', 'coffeeImage.jpg', 8)


def setup(bot):
    bot.add_cog(Text_Memes(bot))  
