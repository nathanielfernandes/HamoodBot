import os
import asyncio
import discord
from discord.ext import commands

from modules.filler_functions import _Filler


class Filler(commands.Cog):
    """Play the Filler Imessage game with an oponent"""

    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.keys = {}
        self.emojis = [
            "\U0001F7E5",
            "\U0001F7E7",
            "\U0001F7E8",
            "\U0001F7E9",
            "\U0001F7E6",
            "\U0001F7EA",
        ]
        self.colors = [
            discord.Color.red(),
            discord.Color.orange(),
            discord.Color.gold(),
            discord.Color.green(),
            discord.Color.blue(),
            discord.Color.purple(),
        ]

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def filler(self, ctx, member: discord.Member = None):
        """``filler [@opponent]`` starts a new filler game (games auto delete if theres no input for 10 minutes)"""
        if member == None or member.bot or member == ctx.author:
            await ctx.send("tag a user you want to play against")
            return

        elif str(ctx.guild.id) + str(member.id) in self.keys:
            await ctx.send("The member you tagged is currently in a game!")
            return

        elif str(ctx.guild.id) + str(ctx.author.id) in self.keys:
            await ctx.send("You are currently in a game!")
            return

        self.keys[str(ctx.guild.id) + str(ctx.author.id)] = (
            str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
        )

        self.keys[str(ctx.guild.id) + str(member.id)] = (
            str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
        )

        # str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
        game_id = self.keys[str(ctx.guild.id) + str(ctx.author.id)]

        if game_id in self.games:
            await self.games[game_id].message.delete()

        self.games[game_id] = _Filler([8, 7], ctx.author, member, ctx.guild)
        embed = discord.Embed(
            title=f"Filler | {ctx.author} vs. {member}",
            description="Loading... :arrows_counterclockwise:",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/699770186227646465/744962953006153738/unknown.png"
        )
        msg = await ctx.send(embed=embed)

        currentGame = self.games[game_id]
        currentGame.message = msg

        for emoji in self.emojis:
            await currentGame.message.add_reaction(emoji)
        await currentGame.message.add_reaction("❌")

        await self.create_fill(game_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            # str(payload.guild_id) + str(payload.user_id)
            key_id = str(payload.guild_id) + str(payload.user_id)
            if key_id in self.keys:
                game_id = self.keys[key_id]

                if game_id in self.games:
                    currentGame = self.games[game_id]

                    if payload.message_id == currentGame.message.id:
                        if str(payload.emoji) in self.emojis:
                            for emoji in self.emojis:
                                if str(payload.emoji) == emoji:
                                    await self.update_game(game_id, emoji, payload)
                        else:
                            if str(payload.emoji) == "❌":
                                await self.create_fill(game_id, True)
                                return

                        await currentGame.message.remove_reaction(
                            member=payload.member, emoji=payload.emoji
                        )

    async def update_game(self, game_id, emoji, payload):
        currentGame = self.games[game_id]
        pick = self.emojis.index(emoji)

        if pick != currentGame.one_pick and pick != currentGame.two_pick:
            if currentGame.turn == 1 and payload.user_id == currentGame.playerOne.id:
                currentGame.one_pick = pick
                await self.create_fill(game_id)
            elif currentGame.turn == -1 and payload.user_id == currentGame.playerTwo.id:
                currentGame.two_pick = pick
                await self.create_fill(game_id)

    async def overtime(self, gameID):
        await asyncio.sleep(300)
        await self.create_fill(gameID, True)

    async def create_fill(self, gameID, delete=False):
        currentGame = self.games[gameID]
        if not delete:
            currentGame.update_player()
            currentGame.draw_board()
            if not currentGame.run_level:
                winner = currentGame.get_winner()
                if winner != False:
                    if winner == currentGame.playerOne:
                        msg = f"{currentGame.sprites[currentGame.one_pick]} {winner} won the game!"
                        colour = self.colors[currentGame.one_pick]
                    elif winner == currentGame.playerTwo:
                        colour = self.colors[currentGame.two_pick]
                        msg = f"{currentGame.sprites[currentGame.two_pick]} {winner} won the game!"
                else:
                    msg = "It's a draw!"
                    colour = discord.Color.default()

                currentGame.timer.cancel()
                self.games.pop(gameID)
                self.keys.pop(
                    str(currentGame.server.id) + str(currentGame.playerOne.id)
                )
                self.keys.pop(
                    str(currentGame.server.id) + str(currentGame.playerTwo.id)
                )
                await currentGame.message.clear_reactions()
            else:
                msg = f"Filler | {currentGame.sprites[currentGame.current_colour]} {currentGame.current_player}'s Turn"

                if currentGame.timer != None:
                    currentGame.timer.cancel()

                currentGame.timer = asyncio.create_task(self.overtime(gameID))
                colour = self.colors[currentGame.current_colour]
            embed = discord.Embed(
                title=msg, description=f"{currentGame.game_grid}", color=colour,
            )
            # embed.set_author(name=f"| Filler |")
            embed.add_field(
                name=f"{currentGame.sprites[currentGame.one_pick]} {currentGame.playerOne}: {currentGame.amountOne}       {currentGame.sprites[currentGame.two_pick]} {currentGame.playerTwo}: {currentGame.amountTwo}",
                value="auto delete in 5 mins",
            )

            await currentGame.message.edit(embed=embed)

        else:
            embed = discord.Embed(title="Filler")
            embed.set_author(name="No Winner")
            embed.set_footer(text="Game was deleted.")
            currentGame.timer.cancel()
            self.games.pop(gameID)
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))

            try:
                await currentGame.message.clear_reactions()
                await currentGame.message.edit(embed=embed)
            except discord.errors.NotFound:
                print("Could not delete Filler game!")


def setup(bot):
    bot.add_cog(Filler(bot))
