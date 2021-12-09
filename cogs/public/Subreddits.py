import os
import random
import discord
from discord.ext import commands
import asyncio

from utils.Premium import PremiumCooldown
from utils.helpers import ReactionController


class Subreddits(commands.Cog):
    """Get Reddit Posts"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.RedditCommands = {
            "memes": ("memes", True, []),
            "dankmemes": ("dankmemes", True, ["dank", "dankmeme"]),
            "cats": ("cats", True, ["cat", "kitten", "kitty", "noura"]),
            "dog": ("dog", True, ["dogs", "doggy", "puppy"]),
            "blessedimages": ("Blessed_Images", True, ["bless", "blessed"]),
            "blursedimages": ("blursedimages", True, ["blursed"]),
            "cursedimages": ("cursedimages", True, ["cursed"]),
            "raimimemes": ("raimimemes", True, ["pizzatime", "ayan"]),
            "minecraft": ("minecraft", True, []),
            "greentext": ("greentext", True, ["greentxt"]),
            "foodporn": ("FoodPorn", True, ["fp", "foodp"]),
            "amitheasshole": ("amitheasshole", False, ["aita", "amitheah"]),
            "programmerhumour": ("ProgrammerHumour", True, ["pgh", "programmer"]),
            "pcmasterrace": ("pcmasterrace", True, ["pcmr"]),
            "bertstrips": ("bertstrips", True, []),
            "im14andthisisdeep": ("im14andthisisdeep", True, ["im14deep"]),
            "eyebleach": ("eyebleach", True, []),
            "art": ("Art", True, []),
            "wallpapers": ("wallpapers", True, []),
            "skamtebord": ("skamtebord", True, []),
            "wallstreetbets": ("wallstreetbets", False, ["wsb"]),
            "baystreetbets": ("Baystreetbets", False, ["bsb"]),
            "sadcringe": ("sadcringe", True, []),
            "crappydesign": ("CrappyDesign", True, []),
            "thebindingofisaac": ("thebindingofisaac", True, ["isaac"]),
            "blackpeopletwitter": ("BlackPeopleTwitter", True, ["bpt"]),
            "showerthoughts": ("Showerthoughts", False, []),
            "battlestations": ("battlestations", True, []),
            "funny": ("funny", True, []),
            "gaming": ("gaming", True, []),
            "aww": ("aww", True, []),
            "pics": ("pics", True, []),
            "egg": ("egg", True, []),
            "bikinibottomtwitter": ("BikiniBottomTwitter", True, ["bbt"]),
            "mildlyinteresting": ("mildlyinteresting", True, []),
        }
        self.allSubs = [value[0] for value in self.RedditCommands.values()]
        self.calm_down = []
        self.calm_cd = commands.CooldownMapping.from_cooldown(
            3, 5, commands.BucketType.user
        )

    def addredditcommands(self):
        for name in self.RedditCommands:
            info = self.RedditCommands[name]

            @commands.command(
                name=name, help=f"|||Get posts from r/{info[0]}", aliases=info[2]
            )
            @commands.check(PremiumCooldown(prem=(3, 5, "user"), reg=(3, 5, "channel")))
            @commands.bot_has_permissions(embed_links=True)
            async def cmd(self, ctx):
                await self.quicksend(
                    ctx,
                    self.RedditCommands[ctx.command.name][0],
                    image=self.RedditCommands[ctx.command.name][1],
                )

            cmd.cog = self
            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            self.bot.add_command(cmd)

    def makeembed(self, post, subreddit=None, allowNSFW=False):
        embed = discord.Embed(color=discord.Color.from_rgb(*self.Hamood.pastel_color()))
        if post:
            if post.is_nsfw and not allowNSFW:
                embed.title = "`NSFW` posts cannot be sent in a non `NSFW` channel"
            else:
                embed.description = post.description
                embed.set_author(name=post.title, url=post.permalink)

                if post.hasimage:
                    embed.set_image(url=post.image_url)
                elif post.thumbnail:
                    embed.set_image(url=post.thumbnail)

            embed.set_footer(
                text=f"r/{post.subreddit} {'⚠️ NSFW ' if post.is_nsfw else ''}• ⇧{post.upvotes:,} upvotes",
                icon_url="https://cdn.discordapp.com/attachments/732309032240545883/756609606922535057/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png",
            )
        else:
            if subreddit is not None:
                embed.title = f"Could not find any posts from `r/{subreddit}`"
            else:
                embed.title = "Could not find that post."

        return embed

    async def quicksend(self, ctx, sub, image=True):
        post = await self.Hamood.Reddit.get_random_post(sub, image)
        embed = self.makeembed(post, sub, ctx.channel.is_nsfw())
        await ctx.reply(embed=embed, mention_author=False)

    def clean_sub(self, sub: str):
        return (sub or random.choice(self.allSubs)).replace("+", "")

    @commands.command(aliases=["r"])
    @commands.check(PremiumCooldown(prem=(3, 5, "user"), reg=(3, 5, "channel")))
    @commands.bot_has_permissions(embed_links=True)
    async def reddit(self, ctx, sub=None):
        """<subreddit>|||Get a post from a SubReddit."""
        await self.quicksend(ctx, self.clean_sub(sub), False)

    @commands.command(aliases=["redpic", "rp"])
    @commands.check(PremiumCooldown(prem=(3, 5, "user"), reg=(3, 5, "channel")))
    @commands.bot_has_permissions(embed_links=True)
    async def redditpic(self, ctx, sub=None):
        """<subreddit>|||Get a post from a SubReddit (only posts with images)."""
        await self.quicksend(ctx, self.clean_sub(sub), True)

    @commands.command()
    @commands.max_concurrency(5, per=commands.BucketType.guild)
    @commands.check(PremiumCooldown(prem=(2, 30, "user"), reg=(2, 30, "channel")))
    @commands.bot_has_permissions(embed_links=True, manage_messages=True)
    async def imagefeed(self, ctx, sub=None):
        """<subreddit>|||Opens a scrollable reddit feed. Filters only images."""
        feed = RedditFeed(ctx, self.bot)
        await feed(subreddit=self.clean_sub(sub), image_only=True)

    @commands.command()
    @commands.max_concurrency(5, per=commands.BucketType.guild)
    @commands.check(PremiumCooldown(prem=(2, 30, "user"), reg=(2, 30, "channel")))
    @commands.bot_has_permissions(embed_links=True, manage_messages=True)
    async def feed(self, ctx, sub=None):
        """<subreddit>|||Opens a scrollable reddit feed."""
        feed = RedditFeed(ctx, self.bot)
        await feed(subreddit=self.clean_sub(sub))

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            self.Hamood.ignore_check(message)
            and message.author.id not in self.calm_down
        ):
            return

        grabbed = self.Hamood.re_RedditUrl.search(message.content)
        if grabbed:
            bucket = self.calm_cd.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                self.calm_down.append(message.author.id)
                await asyncio.sleep(5)
                self.calm_down.remove(message.author.id)
            else:
                post_id = grabbed.group(1)
                post = await self.Hamood.Reddit.fetch_post(post_id=post_id)
                await message.reply(
                    embed=self.makeembed(post, allowNSFW=message.channel.is_nsfw()),
                    mention_author=False,
                )


class RedditFeed(ReactionController):
    def __init__(self, ctx, bot):
        super().__init__()

        self.ctx = ctx
        self.bot = bot

        self.Hamood = bot.Hamood
        self.author = ctx.author

        self.page = 0
        self.prev_page = -1
        self.allowNSFW = ctx.channel.is_nsfw()

        self.dead = False

    def reaction_check(self, reaction, user):
        return (user == self.author) and self.ismapped(str(reaction.emoji))

    def makeembed(self, post, subreddit=None, allowNSFW=False):
        embed = discord.Embed(color=discord.Color.from_rgb(*self.Hamood.pastel_color()))
        if post:
            if post.is_nsfw and not allowNSFW:
                embed.title = "`NSFW` posts cannot be sent in a non `NSFW` channel"
            else:
                embed.description = post.description
                embed.set_author(name=post.title, url=post.permalink)

                if post.hasimage:
                    embed.set_image(url=post.image_url)
                elif post.thumbnail:
                    embed.set_image(url=post.thumbnail)

            embed.set_footer(
                text=f"r/{post.subreddit} {'⚠️ NSFW ' if post.is_nsfw else ''}• ⇧{post.upvotes:,} upvotes",
                icon_url="https://cdn.discordapp.com/attachments/732309032240545883/756609606922535057/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png",
            )
        else:
            if subreddit is not None:
                embed.title = f"Could not find any posts from `r/{subreddit}`"
            else:
                embed.title = "Could not find that post."

        return embed

    def makeembed(self, post, notFound=False):
        embed = discord.Embed(color=discord.Color.from_rgb(*self.Hamood.pastel_color()))
        if post:
            if post.is_nsfw and not self.allowNSFW:
                embed.title = "`NSFW` posts cannot be sent in a non `NSFW` channel"
            else:
                embed.description = f"{post.description[:1980]}{'...' if len(post.description) >= 1980 else ''}"
                embed.set_author(name=post.title, url=post.permalink)

                if post.hasimage:
                    embed.set_image(url=post.image_url)
                elif post.thumbnail:
                    embed.set_image(url=post.thumbnail)

            embed.set_footer(
                text=f"r/{post.subreddit} {'NSFW ' if post.is_nsfw else ''}• ⇧{post.upvotes:,} upvotes • post: {self.page+1}/{self.feed_length}",
                icon_url="https://cdn.discordapp.com/attachments/732309032240545883/756609606922535057/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png",
            )
        else:
            if notFound:
                embed.title = f"Not enough posts were found from `{self.subreddit}`"
            else:
                embed.title = "Could not find that post."

        return embed

    async def __call__(self, subreddit, image_only=False):
        if self.author.id in self.Hamood.active_feeds:
            return await self.Hamood.quick_embed(
                self.ctx,
                title="You aldready have a feed open!",
                description=f"[**jump!**]({self.Hamood.active_feeds[self.author.id]})",
            )

        self.msg = await self.Hamood.quick_embed(
            self.ctx,
            title=f"Loading Feed from `r/{subreddit}` <a:loading:856302946274246697>",
        )

        self.feed = await self.Hamood.Reddit.fetch_feed(subreddit)
        self.subreddit = subreddit

        if not self.feed:
            return await self.msg.edit(
                embed=self.makeembed(post=None),
                mention_author=False,
            )

        self.feed_ids = [
            post_id
            for post_id in self.feed.keys()
            if (self.feed[post_id].hasimage if image_only else True)
        ]
        self.feed_length = len(self.feed_ids)

        if self.feed_length <= 1:
            return await self.msg.edit(
                embed=self.makeembed(post=None, notFound=True),
                mention_author=False,
            )

        self.Hamood.active_feeds[self.author.id] = self.msg.jump_url

        for button in self.buttons:
            await self.msg.add_reaction(button)

        await self.startloop()

    async def startloop(self):
        await self.update_msg()
        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=self.reaction_check, timeout=120.0
                )
            except asyncio.TimeoutError:
                await self.close_page()
                break
            else:
                try:
                    await self.reaction_event(str(reaction.emoji))
                    if self.dead:
                        break
                    await asyncio.sleep(1.3)
                    await self.update_msg()
                except:
                    await self.close_page()
                    break
                else:
                    await self.msg.remove_reaction(str(reaction.emoji), self.author)

    async def update_msg(self):
        if not self.dead and self.page != self.prev_page:
            self.prev_page = int(self.page)
            await self.msg.edit(
                embed=self.makeembed(post=self.feed[self.feed_ids[self.page]]),
                subreddit=self.subreddit,
                allowNSFW=self.allowNSFW,
            )

    @ReactionController.button("🚪", 5)
    async def close_page(self):
        self.dead = True
        try:
            del self.Hamood.active_feeds[self.author.id]
        except:
            pass
        try:
            await self.msg.clear_reactions()
        except:
            pass

    @ReactionController.button("\u23EA", 0)
    async def start_page(self):
        self.page = 0

    @ReactionController.button("\u25B6", 3)
    async def next_page(self):
        self.page = min(self.page + 1, self.feed_length - 1)

    @ReactionController.button("<a:dice:854422487436623873>", 2)
    async def random_page(self):
        self.page = random.choice(
            [i for i in range(self.feed_length) if i != self.prev_page]
        )

    @ReactionController.button("\u25C0", 1)
    async def previous_page(self):
        self.page = max(self.page - 1, 0)

    @ReactionController.button("\u23E9", 4)
    async def end_page(self):
        self.page = self.feed_length - 1


def setup(bot):
    cog = Subreddits(bot)
    bot.add_cog(cog)
    cog.addredditcommands()
