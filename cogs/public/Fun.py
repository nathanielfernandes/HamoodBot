import random, json
import discord
from discord.ext import commands

from utils.Premium import PremiumCooldown


class Fun(commands.Cog):
    """Random Fun Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.data = json.load(open(f"{self.Hamood.filepath}/data/pokemon.json"))
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

    async def get_pokemon_info(self, name_id) -> dict:
        pokejson = await self.Hamood.ahttp.get_json(
            url=f"https://pokeapi.co/api/v2/pokemon/{name_id}"
        )

        if pokejson == {}:
            return
        specjson = await self.Hamood.ahttp.get_json(
            url=f"https://pokeapi.co/api/v2/pokemon-species/{name_id}"
        )

        lore = [
            text["flavor_text"]
            for text in specjson["flavor_text_entries"]
            if text["language"]["name"] == "en"
        ]

        return {
            "name": specjson["name"].title(),
            "id": specjson["id"],
            "color": specjson["color"]["name"],
            "height": f"{pokejson['height']/10} m",
            "weight": f"{pokejson['weight']/10} kg",
            "image": f"https://img.pokemondb.net/artwork/{specjson['name']}.jpg",
            "types": [typ["type"]["name"] for typ in pokejson["types"]],
            "abilities": [
                (a["ability"]["name"]).capitalize() for a in pokejson["abilities"]
            ],
            "stats": {
                (pokejson["stats"][i]["stat"]["name"]).upper(): pokejson["stats"][i][
                    "base_stat"
                ]
                for i in range(len(pokejson["stats"]))
            },
            "lore": lore[random.randint(0, len(lore) - 1)]
            .replace("\x0c", " ")
            .replace("\n", " "),
        }

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
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
    @commands.bot_has_permissions(embed_links=True)
    async def sortinghat(self, ctx):
        """|||Sorts you to one of the Hogwarts houses"""
        houses = ["Gryffindor", "Hufflepuff", "Slytherin", "Ravenclaw"]
        house = random.choice(houses)
        await self.Hamood.quick_embed(
            ctx,
            description=f"{ctx.author.mention}, you belong to the **{house}** house!",
        )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def vibecheck(self, ctx, member: discord.Member = None):
        """|||Vibechecks you."""
        member = ctx.author if not member else member
        random_word = random.choice(self.Hamood.RANDOMWORDS)
        await self.Hamood.quick_embed(
            ctx,
            description=f"{member.mention} your vibe checked out to be **{random_word}** {random.choice(self.Hamood.RANDOMEMOJIS)}",
        )

    @commands.command()
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    @commands.check(PremiumCooldown(prem=(5, 10, "user"), reg=(3, 10, "user")))
    async def vibe(self, ctx, member: discord.Member = None):
        """|||Vibechecks you but better."""
        member = ctx.author if not member else member
        fonts = self.bot.get_cog("Fonts")
        img, color = await fonts.gen_text(
            ctx,
            f"{random.choice(self.Hamood.RANDOMWORDS)} {random.choice(self.Hamood.RANDOMEMOJIS)}",
            ("random", "random", ""),
            False,
        )
        await self.Hamood.quick_embed(
            ctx=ctx,
            description=f"{member.mention} your vibe checked out to be",
            pil_image=img,
            color=discord.Color.from_rgb(*color),
        )

    @commands.command(aliases=["pokedex"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(1, 0, "user"), reg=(2, 5, "user")))
    async def pokemon(self, ctx, name: commands.clean_content):
        """<name|id>|||Get info on a pokemon."""

        pokemon = await self.get_pokemon_info(name)
        if pokemon:
            embed = discord.Embed(
                title=f"{pokemon['name']} {' '.join([str(self.bot.get_emoji(self.data['shorttypes'][typ])) for typ in pokemon['types']])}",
                description=pokemon["lore"],
                color=self.data["colors"][pokemon["color"]],
                url=f"https://pokemondb.net/pokedex/{pokemon['name']}",
            )

            embed.set_author(
                name=f"Pokedex - {pokemon['id']}",
                icon_url="https://cdn.discordapp.com/attachments/699770186227646465/751609285527470261/pokeball_PNG8.png",
            )

            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )

            embed.add_field(
                name="Base Stats:",
                value="\n".join(
                    [
                        f"{stat}: **{pokemon['stats'][stat]}**"
                        for stat in pokemon["stats"].keys()
                    ]
                ),
            )
            embed.add_field(
                name="Properties:",
                value=f"Height: {pokemon['height']}\nWeight: {pokemon['weight']}",
                inline=True,
            )

            embed.add_field(
                name="Abilities:",
                value="\n".join(pokemon["abilities"])
                if pokemon["abilities"] != []
                else "None",
            )
            embed.set_thumbnail(url=pokemon["image"])

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Could not find the pokemon '{name}'.")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(4, 5, "user"), reg=(4, 10, "user")))
    async def pokevibe(self, ctx, member: discord.Member = None):
        """[@mention]|||Find the pokemon your vibing with."""
        member = ctx.author if not member else member

        pokemon = await self.get_pokemon_info(random.randint(1, 893))
        if pokemon:
            embed = discord.Embed(
                title=f"{member} is vibing with **{pokemon['name']}** {' '.join([str(self.bot.get_emoji(self.data['shorttypes'][typ])) for typ in pokemon['types']])}",
                color=self.data["colors"][pokemon["color"]],
            )
            embed.set_author(
                name=f"Pokedex - {pokemon['id']}",
                icon_url="https://cdn.discordapp.com/attachments/699770186227646465/751609285527470261/pokeball_PNG8.png",
            )

            embed.set_image(url=pokemon["image"])

            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(1, 0, "user"), reg=(2, 5, "user")))
    async def pokepic(self, ctx, name: commands.clean_content):
        """<name|id>|||Gets a pic of a pokemon."""
        pokemon = await self.get_pokemon_info(name)
        if pokemon:
            embed = discord.Embed(
                title=f"**{pokemon['name']}** {' '.join([str(self.bot.get_emoji(self.data['shorttypes'][typ])) for typ in pokemon['types']])}",
                color=self.data["colors"][pokemon["color"]],
            )
            embed.set_author(
                name=f"Pokedex - {pokemon['id']}",
                icon_url="https://cdn.discordapp.com/attachments/699770186227646465/751609285527470261/pokeball_PNG8.png",
            )

            embed.set_image(url=pokemon["image"])

            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Could not find the pokemon '{name}'.")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bubblewrap(self, ctx):
        """|||The closest thing to bubble wrap in discord."""
        wrap = "\n".join("||💥||" * 9 for _ in range(9))

        await self.Hamood.quick_embed(
            ctx, description=wrap, footer={"text": "pop away!"}, reply=False
        )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def match(self, ctx, *, content: commands.clean_content):
        """<person1>, <person2>|||Returns a match percentage between two people <3"""
        match = str(random.randint(0, 100))

        content = content.replace(", ", ",").replace(" ,", ",")
        if "," not in content:
            raise commands.UserInputError()

        content = content.split(",")
        left, right = content

        await self.Hamood.quick_embed(
            ctx, description=f"**{left}** and **{right}** are **{match}%** compatible."
        )

    @commands.command(name="8ball")
    @commands.bot_has_permissions(embed_links=True)
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
    @commands.bot_has_permissions(embed_links=True)
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
    @commands.bot_has_permissions(embed_links=True)
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
    @commands.bot_has_permissions(embed_links=True)
    async def choose(self, ctx, *, content: commands.clean_content):
        """<choice1>, <choice2>, [choice3], ...|||Choose between multiple choices."""
        await self.Hamood.quick_embed(
            ctx,
            title=random.choice(content.split(",")).strip(),
        )


def setup(bot):
    bot.add_cog(Fun(bot))
