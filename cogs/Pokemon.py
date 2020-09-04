import sys
import os
import json
import discord
from discord.ext import commands

sys.path.insert(
    1, os.path.split(os.getcwd())[0] + "/" + os.path.split(os.getcwd())[1] + "/modules"
)

import pokemon_get


class Pokemon(commands.Cog):
    """Pokemon Stats"""

    def __init__(self, bot):
        self.bot = bot
        self.data = json.load(
            open(
                f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/pokemon.json"
            )
        )

    @commands.command(alisases=["poke"])
    async def pokedex(self, ctx, name: commands.clean_content):
        """gets a pokemons info"""

        pokemon = pokemon_get.get_all_info(name)
        if pokemon:
            embed = discord.Embed(
                title=f"{pokemon['id']}: {pokemon['name']} {' '.join([str(self.bot.get_emoji(self.data['shorttypes'][typ])) for typ in pokemon['types']])}",
                description=pokemon["lore"],
                color=self.data["colors"][pokemon["color"]],
                url=f"https://pokemondb.net/pokedex/{pokemon['name']}",
            )

            # embed.add_field(name="Lore:", value=pokemon["lore"])
            embed.add_field(
                name="Base Stats:",
                value="\n".join(
                    [
                        f"{stat}: {pokemon['stats'][stat]}"
                        for stat in pokemon["stats"].keys()
                    ]
                ),
            )
            embed.add_field(
                name="Properties:",
                value=f"Height: `{pokemon['height']}`\nWeight: `{pokemon['weight']}`",
                inline=True,
            )

            embed.add_field(
                name="Abilities:",
                value="\n".join(pokemon["abilities"])
                if pokemon["abilities"] != []
                else "None",
            )
            # embed.add_field(name="poke", value=pokemon["pokedex"])
            #   embed.add_field(name="Moves:", value="\n".join(pokemon["moves"]))
            embed.set_thumbnail(url=pokemon["image"])

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Could not find the pokemon '{name}'.")
        # await ctx.send(f"https://img.pokemondb.net/artwork/{name}.jpg")


def setup(bot):
    bot.add_cog(Pokemon(bot))
