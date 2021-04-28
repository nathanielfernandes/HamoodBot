import os
import random
import discord
from discord.ext import commands
import asyncio

# from modules.reddit_functions import findPost, cachePosts, do_cache
import modules.checks as checks
from utils.reddit import Redditing


class Reddit(commands.Cog):
    """Get Reddit Posts"""

    def __init__(self, bot):
        self.bot = bot
        self.common = [
            "memes",
            "dankmemes",
            "cats",
            "cursedimages",
            "blursedimages",
            "Blessed_Images",
            "raimimemes",
            "dog",
            "minecraft",
        ]
        self.names = [
            "meme",
            "dank",
            "cats",
            "cursed",
            "blursed",
            "blessed",
            "pizzatime",
            "dog",
            "minecraft",
        ]
        self.red = Redditing()

        self.buttons = {
            "\u23EA": 0,
            "\u25C0": -1,
            "\u25B6": 1,
            "\u23E9": 200,
            "🚪": 0,
        }

        self.open_feeds = []

    async def to_embed(self, ctx, post, subRedd, extra=""):
        embed = discord.Embed(colour=16729344)

        if post is None:
            embed.title = f"Could not find a recent post from **r/{subRedd}!**"
        else:
            if post["nsfw"] and not ctx.channel.is_nsfw():
                embed.title = "<:nsfw:809897270245326928> `Cannot send NSFW posts in a non NSFW channel!`"
            else:
                embed.title = post["title"]
                embed.url = post["url"]
                embed.description = (
                    f"{post['text'][:1980]}{'...' if len(post['text']) >= 1980 else ''}"
                )
                if self.red.url_contains_image(post["url"]):
                    embed.set_image(url=post["url"])

                embed.set_footer(
                    text=f"⬆{post['upvotes']} | {post['ratio']:0.0%} upvoted\t {extra}",
                    # icon_url=post["author_icon"],
                )

                if post["nsfw"]:
                    embed.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/741384050387714162/809895718403047514/253-2530675_badge-badge-badge-badge-sign.png"
                    )

        embed.set_author(
            name=f"Reddit | r/{subRedd}",
            icon_url="https://cdn.discordapp.com/attachments/732309032240545883/756609606922535057/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png",
        )

        return embed

    async def redditPrep(self, ctx, subRedd, image=True):
        post = await self.red.get_post(subRedd, image)
        embed = await self.to_embed(ctx, post, subRedd)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def imagefeed(self, ctx, redditSub=None):
        if ctx.author.id in self.open_feeds:
            return await ctx.send("`You can only have one open feed at a time`")

        if redditSub == None:
            redditSub = random.choice(self.common)

        post_index = 0
        feed_ids = await self.red.get_feed(redditSub, True)

        if feed_ids is None:
            return await ctx.send(
                embed=discord.Embed(
                    colour=16729344,
                    title=f"Could not find a recent post from **r/{redditSub}!**",
                )
            )

        self.open_feeds.append(ctx.author.id)

        post = self.red.image_posts_cache[redditSub].get(feed_ids[post_index])
        embed = await self.to_embed(
            ctx, post, redditSub, extra=f"post 1/{len(feed_ids)}"
        )

        msg = await ctx.send(embed=embed)

        for button in self.buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: user == ctx.author
                    and reaction.emoji in self.buttons,
                    timeout=120.0,
                )
            except asyncio.TimeoutError:
                self.open_feeds.remove(ctx.author.id)
                return await msg.clear_reactions()
            else:
                if str(reaction.emoji) == "🚪":
                    self.open_feeds.remove(ctx.author.id)
                    return await msg.clear_reactions()

                prevpost = int(post_index)

                if str(reaction.emoji) == "\u23EA":
                    post_index = 0
                elif str(reaction.emoji) == "\u23E9":
                    post_index = len(feed_ids) - 1
                else:
                    post_index += self.buttons[str(reaction.emoji)]
                await msg.remove_reaction(str(reaction.emoji), ctx.author)

                if 0 <= post_index < len(feed_ids):
                    if prevpost != post_index:
                        post = self.red.image_posts_cache[redditSub].get(
                            feed_ids[post_index]
                        )
                        embed = await self.to_embed(
                            ctx,
                            post,
                            redditSub,
                            extra=f"post {post_index+1}/{len(feed_ids)}",
                        )
                        await asyncio.sleep(1)
                        await msg.edit(embed=embed)
                else:
                    post_index = int(prevpost)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def feed(self, ctx, redditSub=None):
        if ctx.author.id in self.open_feeds:
            return await ctx.send("`You can only have one open feed at a time`")

        if redditSub == None:
            redditSub = random.choice(self.common)

        post_index = 0
        feed_ids = await self.red.get_feed(redditSub, False)

        if feed_ids is None:
            return await ctx.send(
                embed=discord.Embed(
                    colour=16729344,
                    title=f"Could not find a recent post from **r/{redditSub}!**",
                )
            )

        self.open_feeds.append(ctx.author.id)

        post = self.red.all_posts_cache[redditSub].get(feed_ids[post_index])
        embed = await self.to_embed(
            ctx, post, redditSub, extra=f"post 1/{len(feed_ids)}"
        )

        msg = await ctx.send(embed=embed)

        for button in self.buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: user == ctx.author
                    and reaction.emoji in self.buttons,
                    timeout=120.0,
                )
            except asyncio.TimeoutError:
                self.open_feeds.remove(ctx.author.id)
                return await msg.clear_reactions()
            else:
                if str(reaction.emoji) == "🚪":
                    self.open_feeds.remove(ctx.author.id)
                    return await msg.clear_reactions()

                prevpost = int(post_index)

                if str(reaction.emoji) == "\u23EA":
                    post_index = 0
                elif str(reaction.emoji) == "\u23E9":
                    post_index = len(feed_ids) - 1
                else:
                    post_index += self.buttons[str(reaction.emoji)]
                await msg.remove_reaction(str(reaction.emoji), ctx.author)

                if 0 <= post_index < len(feed_ids):
                    if prevpost != post_index:
                        post = self.red.all_posts_cache[redditSub].get(
                            feed_ids[post_index]
                        )
                        embed = await self.to_embed(
                            ctx,
                            post,
                            redditSub,
                            extra=f"post {post_index+1}/{len(feed_ids)}",
                        )
                        await msg.edit(embed=embed)
                else:
                    post_index = int(prevpost)

    @commands.command(aliases=["red", "r", "reddit"])
    @checks.isAllowedCommand()
    @commands.cooldown(3, 5, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def redit(self, ctx, redditSub=None):
        """``redit [subreddit]`` finds a post from your specified subreddit"""
        if redditSub == None:
            redditSub = random.choice(self.common)
        await self.redditPrep(ctx, redditSub, False)

    @commands.command(aliases=["redpic", "rp"])
    @checks.isAllowedCommand()
    @commands.cooldown(3, 5, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def redditpic(self, ctx, redditSub=None):
        """``redditpic [subreddit]`` finds a picture post from your specified subreddit"""
        if redditSub == None:
            redditSub = random.choice(self.common)
        await self.redditPrep(ctx, redditSub, True)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def meme(self, ctx):
        """``meme`` quickly sends a meme from r/meme"""
        await self.redditPrep(ctx, "memes")

    # @commands.command()
    # @commands.cooldown(5, 5, commands.BucketType.user)
    # @commands.has_permissions(embed_links=True)
    # async def dark(self, ctx):
    #     """``dark`` quickly sends a meme from r/DarkMemesAndHumor"""
    #     await self.redditPrep(ctx, "DarkMemesAndHumor")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions()
    async def dank(self, ctx):
        """``dank`` quickly sends a meme from r/dankmemes"""
        await self.redditPrep(ctx, "dankmemes")

    @commands.command(aliases=["cats", "noura"])
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def cat(self, ctx):
        """``cat`` quickly sends a cat from r/cats"""
        await self.redditPrep(ctx, "cats")

    @commands.command(aliases=["curse"])
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def cursed(self, ctx):
        """``cursed`` quickly sends a post from r/cursedimages"""
        await self.redditPrep(ctx, "cursedimages")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def blursed(self, ctx):
        """``blursed`` quickly sends a post from r/blursedimages"""
        await self.redditPrep(ctx, "blursedimages")

    @commands.command(aliases=["bless"])
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def blessed(self, ctx):
        """``blessed`` quickly sends a post from r/Blessed_Images"""
        await self.redditPrep(ctx, "Blessed_Images")

    @commands.command(aliases=["pizza", "time", "pizza time", "ayan"])
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def pizzatime(self, ctx):
        """``pizzatime`` its pizza time"""
        await self.redditPrep(ctx, "raimimemes")

    @commands.command(aliases=["dogs", "doggy", "doge"])
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def dog(self, ctx):
        """``dog`` quickly sends a dog from r/dogs"""
        await self.redditPrep(ctx, "dog")

    @commands.command(aliases=["charity", "mine"])
    @checks.isAllowedCommand()
    @commands.cooldown(5, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def minecraft(self, ctx):
        """``minecraft`` quickly sends a dog from r/Minecraft"""
        await self.redditPrep(ctx, "minecraft")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def spam(self, ctx, redditSub="random", amount="3"):
        """``spam [subreddit] [amount]`` sends a number of posts from a specified subreddit (max=10)"""
        amount = int(amount)
        if amount > 5:
            amount = 5

        if redditSub in self.names:
            redditSub = self.common[self.names.index(redditSub)]

        for i in range(amount):
            if redditSub == "random":
                r = random.choice(self.common)
            else:
                r = redditSub
            await self.redditPrep(ctx, r, False)

    # @commands.command()
    # async def rvdl(self, ctx):
    #     """``rvdl``"""
    #     embed = discord.Embed(title=f"Post from r/[subreddit]:", colour=16729344)
    #     embed.set_author(
    #         name="Reddit",
    #         icon_url="https://cdn.discordapp.com/attachments/732309032240545883/756609606922535057/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png",
    #     )
    #     embed.set_footer(
    #         text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
    #     )
    #     embed.set_image(
    #         url="https://cdn.discordapp.com/avatars/485138947115057162/a_a04f5ec2c6d48c9fa298d12c63f62231.gif?size=1024"
    #     )
    #     embed.set_thumbnail(
    #         url="https://cdn.discordapp.com/attachments/749779300181606411/802050446381940786/test3.png"
    #     )

    #     await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
