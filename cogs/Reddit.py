import os
import sys
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import reddit_functions

class Reddit(commands.Cog):
    """Get Reddit Posts"""
    def __init__(self, bot):
        self.bot = bot
        
    async def redditPrep(self, ctx, subRedd):
        async with ctx.typing():
            is_image = False
            while not is_image:
                post = reddit_functions.findPost(subRedd)
                if (".jpg" in post.url) or (".jpeg" in post.url) or (".png" in post.url):
                    is_image = True
            embed = discord.Embed(title=f"Post from r/{subRedd}:", colour=ctx.author.color, url=post.url)
            embed.set_image(url=post.url)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(aliases=['reddit'])
    async def red(self, ctx, redditSub=None):
        """``red [subreddit]`` finds a post from your specified subreddit"""
        if (redditSub == None):
            redditSub = reddit_functions.getSubReddit()
        post = reddit_functions.findPost(redditSub)
        await ctx.send(f"here's your post from the '{redditSub}' subreddit {ctx.author.mention}\n{post.url}")


    @commands.command(aliases=['memes'])
    async def meme(self, ctx):
        """``meme`` quickly sends a meme from r/meme"""
        await self.redditPrep(ctx, 'memes')

    @commands.command(aliases=['cats', 'noura'])
    async def cat(self, ctx):
        """``cat`` quickly sends a cat from r/cats"""
        await self.redditPrep(ctx, 'cats')

    @commands.command(aliases=['curse'])
    async def cursed(self, ctx):
        """``cursed`` quickly sends a post from r/cursedimages"""
        await self.redditPrep(ctx, 'cursedimages')

    @commands.command(aliases=['blur'])
    async def blursed(self, ctx):
        """``blursed`` quickly sends a post from r/blursedimages"""
        await self.redditPrep(ctx, 'blursedimages')

    @commands.command(aliases=['bless'])
    async def blessed(self, ctx):
        """``blessed`` quickly sends a post from r/Blessed_Images"""
        await self.redditPrep(ctx, 'Blessed_Images')

    @commands.command(aliases=['pizza', 'time', 'pizza time', 'ayan'])
    async def pizzatime(self, ctx):
        """its pizza time!"""
        await self.redditPrep(ctx, 'raimimemes')

    @commands.command(aliases=["dogs", "doggy", "doge"])
    async def dog(self, ctx):
        """``dog`` quickly sends a dog from r/dogs"""
        await self.redditPrep(ctx, 'dog')

    @commands.command()
    async def spam(self, ctx, redditSub='random', amount='2'):
        """``spam [subreddit] [amount]`` sends a number of posts from a specified subreddit (max=10)"""
        amount = int(amount)
        if amount > 10:
            amount = 10
        amount = int(amount)
        for i in range(amount):
            if (redditSub == "random"):
                redditSub = reddit_functions.getSubReddit()
            await self.redditPrep(ctx, redditSub)


def setup(bot):
    bot.add_cog(Reddit(bot))  
