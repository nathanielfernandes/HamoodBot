import random
import discord
from discord.ext import commands

from utils.Premium import PremiumCooldown


class Fun(commands.Cog):
    """Random Fun Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

        self.possible_responses = [
            "hell naw",
            "i highley doubt it",
            "how am i supposed to know",
            "i guess its possible",
            "fo sho",
            "maybe",
            "stop asking",
            "yeah",
            "nah",
            "i dont care",
            "ofcourse",
            "not really",
        ]

    @commands.command()
    async def pp(self, ctx, member: discord.Member = None):
        """[@mention]|||check your own or someones pp size."""
        member = ctx.author if not member else member
        pepe = f"8{'='*(random.randint(0, 50))}D"

        await self.Hamood.quick_embed(
            ctx,
            author={"name": f"{member.name}'s pp size", "icon_url": member.avatar_url},
            description=f"**{pepe}**",
            footer={"text": f"{len(pepe)-2} inches"},
            color=discord.Color.purple(),
        )

    @commands.command()
    async def sortinghat(self, ctx):
        """|||Sorts you to one of the Hogwarts houses"""
        houses = ["Gryffindor", "Hufflepuff", "Slytherin", "Ravenclaw"]
        house = random.choice(houses)
        await self.Hamood.quick_embed(
            ctx,
            description=f"{ctx.author.mention}, you belong to the **{house}** house!",
        )

    @commands.command()
    async def vibecheck(self, ctx, member: discord.Member = None):
        """|||Vibechecks you."""
        member = ctx.author if not member else member
        random_word = random.choice(self.Hamood.RANDOMWORDS)
        await self.Hamood.quick_embed(
            ctx,
            description=f"{member.mention} your vibe checked out to be **{random_word}**",
        )

    @commands.command()
    @commands.check(PremiumCooldown(prem=(5, 10, "user"), reg=(3, 10, "user")))
    async def vibe(self, ctx, member: discord.Member = None):
        """|||Vibechecks you but better."""
        member = ctx.author if not member else member
        fonts = self.bot.get_cog("Fonts")
        url, color = await fonts.gen_text(
            ctx, random.choice(self.Hamood.RANDOMWORDS), ("random", "random"), False
        )
        await self.Hamood.quick_embed(
            ctx=ctx,
            description=f"{member.mention} your vibe checked out to be",
            image_url=url,
            color=discord.Color.from_rgb(*color),
        )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bubblewrap(self, ctx):
        """|||The closest thing to bubble wrap in discord."""
        wrap = "\n".join("||💥||" * 9 for _ in range(9))

        await self.Hamood.quick_embed(
            ctx, description=wrap, footer={"text": "pop away!"}, reply=False
        )

    @commands.command()
    async def match(self, ctx, *, content: commands.clean_content):
        """[person1], [person2]|||Returns a match percentage between two people <3"""
        match = str(random.randint(0, 100))

        content = content.replace(", ", ",").replace(" ,", ",")
        if "," not in content:
            raise commands.UserInputError()

        content = content.split(", ")
        left, right = content

        await self.Hamood.quick_embed(
            ctx, description=f"**{left}** and **{right}** are **{match}%** compatible."
        )

    @commands.command(name="8ball")
    async def eightball(self, ctx):
        """|||Hamood shakes his magic 8ball."""
        await self.Hamood.quick_embed(
            ctx,
            author={
                "icon_url": "https://cdn.discordapp.com/attachments/790722696219983902/854424446893948948/game-magic-8-ball-no-text.png",
                "name": random.choice(self.possible_responses),
            },
        )

    @commands.command(aliases=["coin"])
    async def flip(self, ctx):
        """|||Flip a coin."""
        options = (
            (
                "heads",
                "https://upload.wikimedia.org/wikipedia/en/e/e0/Canadian_Dollar_-_obverse.png",
            ),
            (
                "tails",
                "https://upload.wikimedia.org/wikipedia/en/e/ef/Canadian_Dollar_-_reverse.png",
            ),
        )

        choice = random.choice(options)
        await self.Hamood.quick_embed(
            ctx, author={"name": choice[0]}, thumbnail=choice[1]
        )

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, dice: str = "1d6"):
        """<NdN>|||Rolls a dice in NdN format."""
        rolls, limit = map(int, dice.split("d"))
        result = ", ".join(
            f"{random.randint(1, min(limit, 1000))}" for r in range(min(rolls, 10))
        )
        await self.Hamood.quick_embed(
            ctx,
            author={
                "name": result,
                "icon_url": "https://cdn.discordapp.com/emojis/791541710995980308.gif",
            },
        )

    @commands.command()
    async def choose(self, ctx, *, content: commands.clean_content):
        """<choice1>, <choice2>, [choice3], ...|||Choose between multiple choices."""
        await self.Hamood.quick_embed(
            ctx,
            title=random.choice(content.split(",")).strip(),
        )


def setup(bot):
    bot.add_cog(Fun(bot))
