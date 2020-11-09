import asyncio
import discord
from discord.ext import commands

from modules.connect4_functions import Connect_Four


class Connect4(commands.Cog):
    """Play Connect Four with an oponent"""

    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.keys = {}
        self.emojis = [
            "\U0001F550",
            "\U0001F551",
            "\U0001F552",
            "\U0001F553",
            "\U0001F554",
            "\U0001F555",
            "\U0001F556",
        ]
        self.colors = [
            discord.Color.blue(),
            discord.Color.orange(),
            discord.Color.red(),
            discord.Color.gold(),
        ]

    @commands.command()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def connect(self, ctx, member: discord.Member = None):
        """``connect [@opponent]`` starts a new connect 4 game (games auto delete if theres no input for 5 minutes)"""
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

        game_id = self.keys[str(ctx.guild.id) + str(ctx.author.id)]

        if game_id in self.games:
            await self.games[game_id].message.delete()

        self.games[game_id] = Connect_Four([7, 6], ctx.author, member, ctx.guild)
        embed = discord.Embed(
            title=f"Connect 4 | {ctx.author} vs. {member}",
            description="Loading... :arrows_counterclockwise:",
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/749779300181606411/774883799347494942/unknown.png"
        )
        msg = await ctx.send(embed=embed)

        currentGame = self.games[game_id]
        currentGame.message = msg

        for emoji in self.emojis:
            await currentGame.message.add_reaction(emoji)
        await currentGame.message.add_reaction("❌")

        await self.update_embed(game_id)

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
                                await self.update_embed(game_id, True)
                                return

                        await currentGame.message.remove_reaction(
                            member=payload.member, emoji=payload.emoji
                        )

    async def update_game(self, game_id, emoji, payload):
        currentGame = self.games[game_id]
        temp = list(currentGame.grid)
        if payload.user_id == currentGame.current_player.id:
            currentGame.choice = self.emojis.index(emoji) + 1
            currentGame.update_player()
            if currentGame.grid != temp:
                await self.update_embed(game_id)

    async def overtime(self, gameID):
        await asyncio.sleep(300)
        await self.update_embed(gameID, True)

    async def update_embed(self, gameID, delete=False):
        currentGame = self.games[gameID]
        if not delete:
            currentGame.draw_board()
            winner, c = currentGame.check_win()
            if not currentGame.run_level:
                if winner is not None:
                    if winner == "Tie":
                        colour = self.colors[0]
                        msg = "It's a draw!"
                    else:
                        colour = self.colors[c]
                        msg = f"{currentGame.sprites[c]} {winner} won the game!"

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

                msg = f"{currentGame.sprites[2] if currentGame.turn == 1 else currentGame.sprites[3]} {currentGame.current_player}'s Turn"

                if currentGame.timer != None:
                    currentGame.timer.cancel()

                currentGame.timer = asyncio.create_task(self.overtime(gameID))
                colour = self.colors[2] if currentGame.turn == 1 else self.colors[3]
            embed = discord.Embed(
                title=msg, description=f"{currentGame.game_grid}", color=colour,
            )
            embed.set_author(
                name="Connect 4",
                icon_url="https://cdn.discordapp.com/attachments/749779300181606411/774883799347494942/unknown.png",
            )

            embed.add_field(
                name=f"{currentGame.sprites[2]}{currentGame.playerOne}     {currentGame.sprites[3]}{currentGame.playerTwo}",
                value="auto delete in 5 mins",
            )

            await currentGame.message.edit(embed=embed)

        else:
            embed = discord.Embed(title="Connect 4")
            embed.set_author(name="No Winner")
            embed.set_footer(text="Game was deleted.")
            self.games.pop(gameID)
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))

            try:
                await currentGame.message.clear_reactions()
                await currentGame.message.edit(embed=embed)
            except discord.errors.NotFound:
                print("Could not delete Connect 4 game!")

            currentGame.timer.cancel()


def setup(bot):
    bot.add_cog(Connect4(bot))
