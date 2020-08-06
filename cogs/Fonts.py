import os
import sys
import discord
import textwrap
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import image_functions

class Fonts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def textPrep(self, ctx, text, font, font_size, colour, wrap=80):
        async with ctx.typing():
            if text == ():
                return

            font = image_functions.getFont(font)
            
            colour = image_functions.getColour(colour)

            text = [text]
            for i in range(len(text)):
                text[i] = textwrap.wrap(text[i], width=wrap)
                for a in range(1,len(text[i])):
                    text[i][a] = '\n' + text[i][a]
                text[i] = ' '.join(text[i])
            text = text[0]

            name = image_functions.randomNumber()
            name = str(name) + '.png'

            textImg = image_functions.makeText(text, font, font_size, colour, name)
            await ctx.message.delete()
            await ctx.send(file=discord.File(textImg))
        os.remove(textImg)


    @commands.command()
    async def arial(self, ctx, *, content: commands.clean_content):
        """send a message in arial text"""
        await self.textPrep(ctx, content, 'arial', 500, 'black', 100)

    @commands.command(aliases=['craft'])
    async def minecraft(self, ctx, *, content: commands.clean_content):
        """send a message in minecraft text"""
        await self.textPrep(ctx, content, 'minecraft', 500, 'yellow2', 100)

    @commands.command(aliases=['tale'])
    async def undertale(self, ctx, *, content: commands.clean_content):
        """send a message in undertale text"""
        await self.textPrep(ctx, content, 'undertale', 500, 'white', 100)

    @commands.command(aliases=['rick'])
    async def morty(self, ctx, *, content: commands.clean_content):
        """send a message in morty text"""
        await self.textPrep(ctx, content, 'morty', 500, 'green1', 100)

    @commands.command()
    async def gta(self, ctx, *, content: commands.clean_content):
        """send a message in starwars text"""
        await self.textPrep(ctx, content, 'gta', 500, 'white', 100)

    @commands.command()
    async def enchant(self, ctx, *, content: commands.clean_content):
        """send a message in enchant text"""
        await self.textPrep(ctx, content, 'enchant', 500, 'minecraft-enchantment.ttf', 100)

    @commands.command(aliases=['?'])
    async def unknown(self, ctx, *, content: commands.clean_content):
        """send a message in unknown text"""
        await self.textPrep(ctx, content, 'unown.ttf', 500, 'black', 100)

    @commands.command(aliases=['poke'])
    async def pokemon(self, ctx, *, content: commands.clean_content):
        """send a message in pokemon text"""
        await self.textPrep(ctx, content, 'pokemon', 500, 'steelblue2', 100)

    @commands.command(aliases=['sonic'])
    async def sega(self, ctx, *, content: commands.clean_content):
        """send a message in sega text"""
        await self.textPrep(ctx, content, 'sega', 500, 'navy', 100)

    @commands.command(aliases=['sponge'])
    async def spongebob(self, ctx, *, content: commands.clean_content):
        """send a message in spongebob text"""
        await self.textPrep(ctx, content, 'spongebob', 500, 'lightblue', 100)

    @commands.command()
    async def avenger(self, ctx, *, content: commands.clean_content):
        """sends a message in avengers text"""
        await self.textPrep(ctx, content, 'avenger', 500, 'red4', 100)

    @commands.command()
    async def sketch(self, ctx, *, content: commands.clean_content):
        """sends a message in avengers text"""
        await self.textPrep(ctx, content, 'sketch', 500, 'random', 100)

    @commands.command()
    async def batman(self, ctx, *, content: commands.clean_content):
        """sends a message in avengers text"""
        await self.textPrep(ctx, content, 'batman', 500, 'black', 100)

    @commands.command()
    async def text(self, ctx, *, content: commands.clean_content):
        """send a message in a random font"""
        await self.textPrep(ctx, content, 'random', 500, 'random', 100)

    @commands.command()
    async def font(self, ctx, font, colour, *, content: commands.clean_content):
        """send a message in a selected font and colour"""
        await self.textPrep(ctx, content, font, 500, colour, 100)


def setup(bot):
    bot.add_cog(Fonts(bot))  