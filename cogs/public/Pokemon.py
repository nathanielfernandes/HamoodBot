import os
import json
import random
import discord
from discord.ext import commands


class Pokemon(commands.Cog):
    """Pokemon Stats"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.data = json.load(open(f"{self.Hamood.filepath}/data/pokemon.json"))

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
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def pokedex(self, ctx, name: commands.clean_content):
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
    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
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
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
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


def setup(bot):
    bot.add_cog(Pokemon(bot))
