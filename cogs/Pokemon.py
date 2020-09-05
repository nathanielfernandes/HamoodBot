import sys
import os
import json
import random
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

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def pokedex(self, ctx, name: commands.clean_content):
        """``pokedex [name or id]`` gets a pokemons info"""

        pokemon = pokemon_get.get_all_info(name)
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

            # embed.add_field(name="Lore:", value=pokemon["lore"])
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
    @commands.has_permissions(embed_links=True)
    async def pokevibe(self, ctx, member: discord.Member = None):
        """``pokevibe [@user]`` finds the pokemon your vibing with"""
        member = ctx.author if not member else member

        pokemon = pokemon_get.get_all_info(random.randint(1, 893))
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
    async def poketype(self, ctx):
        """``poketype`` find your pokemon types"""

        await ctx.send(
            f"{self.bot.get_emoji(random.choice(list(self.data['types'].values())))}{self.bot.get_emoji(random.choice(list(self.data['types'].values())))}"
        )


def setup(bot):
    bot.add_cog(Pokemon(bot))
