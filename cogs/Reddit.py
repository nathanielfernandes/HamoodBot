import os
import random
import discord
from discord.ext import commands

from modules.reddit_functions import findPost, getSubReddit


class Reddit(commands.Cog):
    """Get Reddit Posts"""

    def __init__(self, bot):
        self.bot = bot

    async def redditPrep(self, ctx, subRedd):
        async with ctx.typing():
            is_image = False
            while not is_image:
                post = findPost(subRedd)
                if (
                    (".jpg" in post.url)
                    or (".jpeg" in post.url)
                    or (".png" in post.url)
                ):
                    is_image = True

            embed = discord.Embed(title=f"Post from r/{subRedd}:", colour=16729344)
            embed.set_author(
                name="Reddit",
                icon_url="https://cdn.discordapp.com/attachments/732309032240545883/756609606922535057/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png",
            )
            embed.set_image(url=post.url)
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
        await ctx.send(embed=embed)

    @commands.command(aliases=["reddit"])
    @commands.has_permissions(embed_links=True)
    async def red(self, ctx, redditSub=None):
        """``red [subreddit]`` finds a post from your specified subreddit"""
        if redditSub == None:
            redditSub = getSubReddit()
        post = findPost(redditSub)
        await ctx.send(
            f"here's your post from the '{redditSub}' subreddit {ctx.author.mention}\n{post.url}"
        )

    @commands.command(aliases=["memes"])
    @commands.has_permissions(embed_links=True)
    async def meme(self, ctx):
        """``meme`` quickly sends a meme from r/meme"""
        await self.redditPrep(ctx, "memes")

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def dark(self, ctx):
        """``dark`` quickly sends a meme from r/DarkMemesAndHumor"""
        await self.redditPrep(ctx, "DarkMemesAndHumor")

    @commands.command()
    @commands.has_permissions()
    async def dank(self, ctx):
        """``dank`` quickly sends a meme from r/dankmemes"""
        await self.redditPrep(ctx, "dankmemes")

    @commands.command(aliases=["cats", "noura"])
    @commands.has_permissions(embed_links=True)
    async def cat(self, ctx):
        """``cat`` quickly sends a cat from r/cats"""
        await self.redditPrep(ctx, "cats")

    @commands.command(aliases=["curse"])
    @commands.has_permissions(embed_links=True)
    async def cursed(self, ctx):
        """``cursed`` quickly sends a post from r/cursedimages"""
        await self.redditPrep(ctx, "cursedimages")

    @commands.command(aliases=["blur"])
    @commands.has_permissions(embed_links=True)
    async def blursed(self, ctx):
        """``blursed`` quickly sends a post from r/blursedimages"""
        await self.redditPrep(ctx, "blursedimages")

    @commands.command(aliases=["bless"])
    @commands.has_permissions(embed_links=True)
    async def blessed(self, ctx):
        """``blessed`` quickly sends a post from r/Blessed_Images"""
        await self.redditPrep(ctx, "Blessed_Images")

    @commands.command(aliases=["pizza", "time", "pizza time", "ayan"])
    @commands.has_permissions(embed_links=True)
    async def pizzatime(self, ctx):
        """its pizza time!"""
        await self.redditPrep(ctx, "raimimemes")

    @commands.command(aliases=["dogs", "doggy", "doge"])
    @commands.has_permissions(embed_links=True)
    async def dog(self, ctx):
        """``dog`` quickly sends a dog from r/dogs"""
        await self.redditPrep(ctx, "dog")

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def spam(self, ctx, redditSub="random", amount="1"):
        """``spam [subreddit] [amount]`` sends a number of posts from a specified subreddit (max=10)"""
        amount = int(amount)
        if amount > 5:
            amount = 5
        amount = int(amount)
        for i in range(amount):
            if redditSub == "random":
                redditSub = getSubReddit()
            await self.redditPrep(ctx, redditSub)


def setup(bot):
    bot.add_cog(Reddit(bot))
