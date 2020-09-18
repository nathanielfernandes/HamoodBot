import os
import asyncio
import json
import discord
from discord.ext import commands

from modules.sokoban_functions import Soko_ban


class Sokoban(commands.Cog):
    """A simple box pushing game"""

    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.info = json.load(
            open(
                f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/sokoban.json"
            )
        )
        self.themes = self.info["themes"]
        self.emoji_dict = self.info["emojis"]

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def sokoban(self, ctx):
        """``sokoban`` starts a new sokoban game (games auto delete if theres no input for 10 minutes)"""
        game_id = str(ctx.guild.id) + str(
            ctx.author.id
        )  # if ctx.guild != None else str(ctx.author.id)

        if game_id in self.games:
            await self.games[game_id].message.delete()

        # max [9, 7]
        self.games[game_id] = Soko_ban([5, 3], ctx.author, None)
        embed = discord.Embed(
            title=f"Sokoban | {ctx.author}",
            description="Loading... :arrows_counterclockwise:",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/699770186227646465/744963999782797512/unknown.png"
        )
        msg = await ctx.send(embed=embed)
        # await ctx.send(f"{ctx.author.mention}'s Game:")

        currentGame = self.games[game_id]
        currentGame.message = msg
        currentGame.sprites = self.themes[currentGame.theme_num]

        for emoji in self.emoji_dict:
            await currentGame.message.add_reaction(emoji)

        await currentGame.message.add_reaction("\U0001F440")
        await currentGame.message.add_reaction("❌")

        await self.create_board(game_id)

    @commands.Cog.listener()
    @commands.has_permissions(embed_links=True)
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            game_id = str(payload.guild_id) + str(payload.user_id)

            if game_id in self.games:
                currentGame = self.games[game_id]

                if payload.message_id == currentGame.message.id:
                    if str(payload.emoji) in self.emoji_dict:
                        for emoji in self.emoji_dict:
                            if str(payload.emoji) == emoji:
                                currentGame.move = self.emoji_dict[emoji]
                                await currentGame.message.remove_reaction(
                                    member=currentGame.user, emoji=emoji
                                )
                    else:
                        if str(payload.emoji) == "\U0001F440":
                            currentGame.move = None

                            currentGame.theme_num += 1
                            if currentGame.theme_num >= len(self.themes):
                                currentGame.theme_num = 0

                            currentGame.sprites = self.themes[currentGame.theme_num]
                            await currentGame.message.remove_reaction(
                                member=currentGame.user, emoji="\U0001F440"
                            )
                        elif str(payload.emoji) == "❌":
                            await self.create_board(game_id, True)
                            return
                        elif str(payload.emoji) == "\u23E9":
                            currentGame.move = "next"
                            await currentGame.message.remove_reaction(
                                member=currentGame.user, emoji="\u23E9"
                            )

                    await self.create_board(game_id)

    async def overtime(self, gameID):
        await asyncio.sleep(600)
        await self.create_board(gameID, True)

    async def create_board(self, gameID, delete=False):
        currentGame = self.games[gameID]
        if not delete:
            currentGame.player_move()
            currentGame.draw_board()
            if not currentGame.run_level:
                currentGame.game_start()
                msg = f"Click Any Button To Go To Level {currentGame.level}:"
                currentGame.moves -= 1
            else:
                msg = f"{currentGame.user}'s game | Level {currentGame.level}:"

            embed = discord.Embed(
                title=msg,
                description=f"{currentGame.game_grid}",
                color=currentGame.user.color,
            )
            embed.set_author(
                name="Sokoban",
                icon_url="https://cdn.discordapp.com/attachments/699770186227646465/744963999782797512/unknown.png",
            )
            embed.add_field(
                name=f"{currentGame.sprites[2]} Boxes Left: {len(currentGame.box_pos) - currentGame.completed}     {currentGame.sprites[5]} Moves: {currentGame.moves}",
                value="auto delete in 10 mins",
            )

            await currentGame.message.edit(embed=embed)

            if currentGame.timer != None:
                currentGame.timer.cancel()

            currentGame.timer = asyncio.create_task(self.overtime(gameID))
        else:
            embed = discord.Embed(title="Sokoban")
            embed.set_author(
                name=f"{currentGame.user} made it to level {currentGame.level}!",
                icon_url=currentGame.user.avatar_url,
            )
            embed.set_footer(text="Game was deleted.")
            currentGame.timer.cancel()
            self.games.pop(gameID)

            try:
                await currentGame.message.clear_reactions()
                await currentGame.message.edit(embed=embed)
            except discord.errors.NotFound:
                print("Could not delete Sokoban game!")


def setup(bot):
    bot.add_cog(Sokoban(bot))

