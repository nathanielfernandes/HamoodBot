import os
import json
import random
import discord
from discord.ext import commands

from modules.pokemon_get import get_pokemon_info
import modules.checks as checks


class Pokemon(commands.Cog):
    """Pokemon Stats"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.data = json.load(open(f"{self.Hamood.filepath}/data/pokemon.json"))

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def pokedex(self, ctx, name: commands.clean_content):
        """``pokedex [name or id]`` gets a pokemons info"""

        pokemon = get_pokemon_info(name)
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
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def pokevibe(self, ctx, member: discord.Member = None):
        """``pokevibe [@user]`` finds the pokemon your vibing with"""
        member = ctx.author if not member else member

        pokemon = get_pokemon_info(random.randint(1, 893))
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
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def pokepic(self, ctx, name: commands.clean_content):
        """``pokepic [pokemon]`` gets a pic of the pokemon"""
        pokemon = get_pokemon_info(name)
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

    # @commands.command()
    # async def poketype(self, ctx):
    #     """``poketype`` find your pokemon types"""

    #     await ctx.send(
    #         f"{self.bot.get_emoji(random.choice(list(self.data['types'].values())))}{self.bot.get_emoji(random.choice(list(self.data['types'].values())))}"
    #     )


def setup(bot):
    bot.add_cog(Pokemon(bot))
