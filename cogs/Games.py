import os
import json
import asyncio
import discord
from discord.ext import commands

from modules.games.filler_functions import _Filler
from modules.games.connect4_functions import Connect_Four
from modules.games.sokoban_functions import Soko_ban
from modules.games.twentyforty8_functions import TwentyFortyEight
from modules.games.chess_functions import _Chess
from modules.games.trivia_functions import _Trivia
import modules.checks as checks


class Games(commands.Cog):
    """Play Games, all games auto delete if theres no input for 2 minutes"""

    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.keys = {}
        self.games_log = {}
        self.game_names = ["total", "filler", "connect4", "chess"]

        self.leaderboard_emojis = [
            ":first_place:",
            ":second_place:",
            ":third_place:",
            ":clap:",
            ":clap:",
            ":clap:",
            ":thumbsup:",
            ":thumbsup:",
            ":thumbsup:",
            ":poop:",
        ]
        self.info = json.load(
            open(
                f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/sokoban.json"
            )
        )
        self.chessEmojis = {"none": "none"}

        self.triviaEmojis = {
            "<:chessA:776347125272412161>": 0,
            "<:chessB:776347122341249044>": 1,
            "<:chessC:776347121694539777>": 2,
            "<:chessD:776347122496831498>": 3,
        }

        self.twenty48Emojis = {
            "\u2B05": "left",
            "\u2B06": "up",
            "\u2B07": "down",
            "\u27A1": "right",
        }

        self.themes = self.info["themes"]
        self.sokobanEmojis = {
            "\u2B05": "left",
            "\u2B06": "up",
            "\u2B07": "down",
            "\u27A1": "right",
            "\u21A9": "reset",
            "\u267B": "shuffle",
            "\U0001F440": "theme",
        }

        self.fillerEmojis = {
            "<:red:782108442998997003>": 0,
            "<:blue:782108442851803158>": 1,
            "<:green:782108443418689536>": 2,
            "<:yellow:782108443225751552>": 3,
            "<:purple:782108443284733962>": 4,
            "<:black:782108442835812374>": 5,
        }

        self.fillerColors = [
            discord.Color.from_rgb(229, 43, 92),
            discord.Color.from_rgb(56, 158, 220),
            discord.Color.from_rgb(166, 227, 90),
            discord.Color.from_rgb(251, 235, 62),
            discord.Color.from_rgb(115, 79, 166),
            discord.Color.from_rgb(64, 64, 64),
        ]

        self.connectEmojis = {
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5,
            "6️⃣": 6,
            "7️⃣": 7,
        }

        self.connectColors = [
            discord.Color.blue(),
            discord.Color.orange(),
            discord.Color.red(),
            discord.Color.gold(),
        ]

        self.gameCalls = {
            "update_trivia_embed": self.update_trivia_embed,
            "update_trivia_game": self.update_trivia_game,
            "triviaEmojis": self.triviaEmojis,
            "chessEmojis": self.chessEmojis,
            "update_2048_game": self.update_2048_game,
            "update_2048_embed": self.update_2048_embed,
            "2048Emojis": self.twenty48Emojis,
            "update_sokoban_game": self.update_sokoban_game,
            "update_sokoban_embed": self.update_sokoban_embed,
            "sokobanEmojis": self.sokobanEmojis,
            "update_connect4_game": self.update_connect_game,
            "update_connect4_embed": self.update_connect_embed,
            "connect4Emojis": self.connectEmojis,
            "update_filler_game": self.update_filler_game,
            "update_filler_embed": self.update_filler_embed,
            "fillerEmojis": self.fillerEmojis,
        }

    async def update_leaderboards(self, guild_id, game, member_won_id, member_lost_id):
        await self.bot.leaderboards.add_leaderboard(guild_id)

        await self.bot.leaderboards.add_member(guild_id, member_won_id)
        await self.bot.leaderboards.add_member(guild_id, member_lost_id)

        await self.bot.leaderboards.add_game(guild_id, member_won_id, game)
        await self.bot.leaderboards.add_game(guild_id, member_lost_id, game)

        await self.bot.leaderboards.incr_game_won(guild_id, member_won_id, game)
        await self.bot.leaderboards.incr_game_lost(guild_id, member_lost_id, game)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            key_id = str(payload.guild_id) + str(payload.user_id)
            if key_id in self.keys:
                game_id = self.keys[key_id]
                if game_id in self.games:
                    currentGame = self.games[game_id]

                    if payload.message_id == currentGame.message.id:
                        gameType = game_id[: game_id.index("#")]

                        if str(payload.emoji) in self.gameCalls[f"{gameType}Emojis"]:
                            move = self.gameCalls[f"{gameType}Emojis"][
                                str(payload.emoji)
                            ]
                            currentGame.game_started = True
                            await self.gameCalls[f"update_{gameType}_game"](
                                game_id, move, payload
                            )
                        else:
                            if str(payload.emoji) == "❌":
                                await self.delete_game(
                                    game_id,
                                    f"{payload.member.name} closed the game",
                                    payload.member,
                                )
                                return

                        await currentGame.message.remove_reaction(
                            member=payload.member, emoji=payload.emoji
                        )

    async def init_game(self, ctx, member=None, identifier=None):
        if str(ctx.guild.id) + str(ctx.author.id) in self.keys:
            await ctx.send(
                "You are currently in a game! Use `.leave` to leave ur current game"
            )
            return None

        if "!" in identifier:
            self.keys[str(ctx.guild.id) + str(ctx.author.id)] = (
                identifier + str(ctx.guild.id) + str(ctx.author.id)
            )
        else:
            if member == None or member.bot or member == ctx.author:
                await ctx.send("tag a user you want to play against")
                return None

            elif str(ctx.guild.id) + str(member.id) in self.keys:
                await ctx.send("The member you tagged is currently in a game!")
                return None

            self.keys[str(ctx.guild.id) + str(ctx.author.id)] = (
                identifier + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
            )

            self.keys[str(ctx.guild.id) + str(member.id)] = (
                identifier + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
            )

        game_id = self.keys[str(ctx.guild.id) + str(ctx.author.id)]
        if game_id in self.games:
            await self.games[game_id].message.delete()

        return game_id

    async def overtime(self, gameID, extras="No Winner"):
        self.games_log[f"ID:{gameID}"] = f"{gameID[: gameID.index('#')]}"
        await asyncio.sleep(120)
        await self.delete_game(gameID, extras)

    async def close_game(self, gameID):
        gameType = gameID[: gameID.index("#")]
        currentGame = self.games[gameID]

        self.games.pop(gameID)
        if "!" not in gameID:
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))
        else:
            self.keys.pop(str(currentGame.server.id) + str(currentGame.user.id))
        try:
            await currentGame.message.clear_reactions()
        except discord.errors.NotFound:
            return

    async def delete_game(self, gameID, extras="Timed Out", member=None):
        gameType = gameID[: gameID.index("#")]
        try:
            currentGame = self.games[gameID]
        except KeyError:
            return

        await self.close_game(gameID)
        if "!" not in gameID:
            if currentGame.game_started:
                if member is None:
                    if currentGame.current_player.id == currentGame.playerOne.id:
                        winner = currentGame.playerTwo
                        loser = currentGame.playerOne
                    else:
                        winner = currentGame.playerOne
                        loser = currentGame.playerTwo

                elif member.id == currentGame.playerOne.id:
                    winner = currentGame.playerTwo
                    loser = currentGame.playerOne
                else:
                    winner = currentGame.playerOne
                    loser = currentGame.playerTwo

                await self.update_leaderboards(
                    currentGame.server.id, gameType, winner.id, loser.id
                )
                extras = f"{winner.name} won by defualt!"
            else:
                extras = f"No Winner"
            content = None
        else:
            content = " "
        embed = discord.Embed(title=gameType.capitalize())
        embed.set_author(name=extras)
        embed.set_footer(text="Game was deleted.")

        try:
            await currentGame.message.edit(embed=embed, content=content)
        except discord.errors.NotFound:
            print(f"Could not delete {gameType} game!")

        currentGame.timer.cancel()

    async def add_reactions(self, msg, emojis):
        for emoji in emojis:
            await msg.add_reaction(emoji)
        await msg.add_reaction("❌")

    @commands.command()
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def leave(self, ctx):
        """``leave`` leaves any game you are currently in."""
        key = str(ctx.guild.id) + str(ctx.author.id)
        if key not in self.keys:
            await ctx.send("You are not currently in a game!")
            return

        await self.delete_game(
            self.keys[key], f"{ctx.author.name} closed the game", ctx.author
        )
        await ctx.send(f"{ctx.author.mention}, you have left your game!")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def leaderboard(self, ctx, game="total", stat="won"):
        """``leaderboard [game] [stat]`` a leaderboard of the servers players"""
        leaderboard = await self.bot.leaderboards.get(ctx.guild.id)

        if leaderboard is None:
            return await ctx.send("`No games have been played on this server`")

        game = game.lower()
        stat = stat.lower()

        if game in self.game_names:
            game = game
        elif game in ["connect", "connectfour"]:
            game = "connect4"
        elif game == "all":
            game = "total"
        else:
            return await ctx.send(
                "`Invalid Leaderboard Game Field` (`all`, `filler`, `chess`, `connect`)"
            )

        if stat in ["won", "wins", "win"]:
            stat = "won"
        elif stat in ["lose", "lost"]:
            stat = "lost"
        elif stat in ["skill", "rank"]:
            stat = "skill"
        else:
            return await ctx.send(
                "`Invalid Leaderboard Stat Field` (`won`, `lost`, `skill`)"
            )

        server_leaderboard = []
        if stat != "skill":
            for member_id in leaderboard:
                try:
                    if member_id != "_id" and leaderboard[member_id][game][stat] != 0:
                        server_leaderboard.append(
                            [
                                leaderboard[member_id][game][stat],
                                str(self.bot.get_user(int(member_id))),
                            ]
                        )
                except KeyError:
                    pass
        else:
            for member_id in leaderboard:
                try:
                    if member_id != "_id" and leaderboard[member_id][game]["won"] != 0:
                        server_leaderboard.append(
                            [
                                int(
                                    (
                                        leaderboard[member_id][game]["won"]
                                        / (leaderboard[member_id][game]["lost"] + 1)
                                    )
                                    * 100
                                ),
                                str(self.bot.get_user(int(member_id))),
                            ]
                        )
                except KeyError:
                    pass

        players = len(server_leaderboard)
        if players > 10:
            players = 10
        elif players == 0:
            return await ctx.send("`not enough games have been played`")

        server_leaderboard = sorted(server_leaderboard)
        if stat == "lost":
            server_leaderboard = server_leaderboard[:players]
        else:
            server_leaderboard = server_leaderboard[::-1][:players]

        for i in range(len(server_leaderboard)):
            server_leaderboard[
                i
            ] = f"{self.leaderboard_emojis[i]} {server_leaderboard[i][0]} - {server_leaderboard[i][1]}"

        desc = "\n".join(server_leaderboard)

        embed = discord.Embed(
            title=f"Top {players} in this server ranked by {stat} - {game.capitalize()} Games",
            description=f"{desc}",
            color=discord.Color.gold(),
            timestamp=ctx.message.created_at,
        )

        await ctx.send(embed=embed)

    # @commands.command()
    # @commands.is_owner()
    # async def gameslog(self, ctx):
    #     log = "\n".join([f"{self.games_log[k]} | {k}" for k in self.games_log])
    #     await ctx.send(f"```{len(self.games_log)} Games:\n{log}```")
    # -------------------------------------------------------------------------------------------------------#
    # @commands.command()
    # @checks.isAllowedCommand()
    # @commands.cooldown(2, 60, commands.BucketType.channel)
    # @commands.has_permissions(embed_links=True)
    # async def trivia(self, ctx, member: discord.Member = None):
    #     game_id = await self.init_game(ctx, member=member, identifier="trivia#")
    #     if game_id is None:
    #         return

    #     self.games[game_id] = _Trivia(ctx.author, member, ctx.guild)
    #     embed = discord.Embed(
    #         title=f"Trivia | {ctx.author} vs. {member}",
    #         description="Loading... :arrows_counterclockwise:",
    #     )
    #     embed.set_thumbnail(
    #         url="https://cdn.discordapp.com/attachments/749779300181606411/776368591557754910/unknown.png"
    #     )

    #     msg = await ctx.send(embed=embed)
    #     currentGame = self.games[game_id]
    #     currentGame.message = msg

    #     await self.add_reactions(currentGame.message, self.triviaEmojis)
    #     await self.update_trivia_embed(game_id)

    async def update_trivia_game(self):
        pass

    # async def update_connect_game(self, game_id, move, payload):
    #     currentGame = self.games[game_id]
    #     temp = list(currentGame.grid)
    #     if payload.user_id == currentGame.current_player.id:
    #         currentGame.choice = move
    #         currentGame.update_player()
    #         if currentGame.grid != temp:
    #             await self.update_connect_embed(game_id)

    async def update_trivia_embed(self, gameID):
        currentGame = self.games[gameID]

        currentGame.next_question()
        if currentGame.question_num == 10:
            if (
                currentGame.score[currentGame.playerOne.id]
                == currentGame.score[currentGame.playerTwo.id]
            ):
                msg = "It's a draw!"
            else:
                if (
                    currentGame.score[currentGame.playerOne.id]
                    > currentGame.score[currentGame.playerTwo.id]
                ):
                    winner = currentGame.playerOne
                    loser = currentGame.playerTwo
                elif (
                    currentGame.score[currentGame.playerOne.id]
                    < currentGame.score[currentGame.playerTwo.id]
                ):
                    winner = currentGame.playerTwo
                    loser = currentGame.playerOne

                msg = f"{winner} won the game!"

            currentGame.timer.cancel()
            await self.close_game(gameID)
        else:
            msg = f"Question {currentGame.question_num+1}/10"

            if currentGame.timer is not None:
                currentGame.timer.cancel()

            currentGame.timer = asyncio.create_task(self.overtime(gameID))

        embed = discord.Embed(
            title=msg,
            description=f"**{currentGame.current_question['question']}**\nCategory: {currentGame.current_question['category']}\nDifficulty: {currentGame.current_question['difficulty']}",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name=f"Choices",
            value=f"{currentGame.current_question['options_str']}",
            inline=False,
        )

        embed.set_author(
            name="Trivia",
            icon_url="https://cdn.discordapp.com/attachments/749779300181606411/774883799347494942/unknown.png",
        )

        embed.add_field(
            name=f"{currentGame.playerOne}: **{currentGame.score[currentGame.playerOne.id]}**     {currentGame.playerTwo}: **{currentGame.score[currentGame.playerTwo.id]}**",
            value="auto delete in 2 mins",
            inline=False,
        )

        await currentGame.message.edit(embed=embed)

    # -------------------------------------------------------------------------------------------------------#

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def chess(self, ctx, member: discord.Member = None):
        """``chess [@opponent]`` starts a new chess game. Use .move to play `BETA`"""
        game_id = await self.init_game(ctx, member=member, identifier="chess#")
        if game_id is None:
            return

        self.games[game_id] = _Chess(ctx.author, member, ctx.guild)
        embed = discord.Embed(
            title=f"Chess | <:B_:776325516096569384>{ctx.author} vs. <:W_:776325516118065152>{member}",
            description="Loading... :arrows_counterclockwise:",
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/749779300181606411/776368591557754910/unknown.png"
        )
        msg = await ctx.send(content="Use `.move` to begin.", embed=embed)

        currentGame = self.games[game_id]
        currentGame.message = msg

        await msg.add_reaction("❌")

        await self.update_chess_embed(game_id)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def move(self, ctx, *, content: commands.clean_content = None):
        """``chess [coordinate of peice] [coordinate to move peice to]`` can only be used if you are in a chess match!. """
        if str(ctx.guild.id) + str(ctx.author.id) not in self.keys:
            await ctx.send("You are not currently in a game!")
            return

        invalid_move = None

        game_id = self.keys[str(ctx.guild.id) + str(ctx.author.id)]
        currentGame = self.games[game_id]

        if ctx.author.id == currentGame.current_player[currentGame.turn].id:
            currentGame.move = content.lower().replace(" ", "").replace(",", "")
            msg = await currentGame.update_game()
            if msg is not None:
                invalid_move = await ctx.send(msg)
            else:
                await self.update_chess_embed(game_id)
                currentGame.game_started = True
        else:
            invalid_move = await ctx.send("It's not your turn!")

        if invalid_move is not None:
            await invalid_move.add_reaction("<:trash:783097450461397052>")

        await ctx.message.delete()

    async def update_chess_embed(self, gameID):
        currentGame = self.games[gameID]

        currentGame.draw_board()
        currentGame.check_end()
        if not currentGame.run_game:
            if currentGame.winner == "DRAW":
                msg = "Draw"
            else:
                if currentGame.winner == -1:
                    msg = f"<:W_:776325516118065152>{currentGame.current_player[-1]} won by {currentGame.reason}"
                    colour = discord.Color.from_rgb(245, 245, 220)
                    winner = currentGame.current_player[-1]
                    loser = currentGame.current_player[1]

                elif currentGame.winner == 1:
                    msg = f"<:B_:776325516096569384>{currentGame.current_player[1]} won by {currentGame.reason}"
                    colour = discord.Color.blue()
                    winner = currentGame.current_player[1]
                    loser = currentGame.current_player[-1]

                await self.update_leaderboards(
                    currentGame.server.id, "chess", winner.id, loser.id
                )
            currentGame.timer.cancel()
            await self.close_game(gameID)
        else:
            msg = f"{'<:B_:776325516096569384>' if currentGame.turn == 1 else '<:W_:776325516118065152>'} {currentGame.current_player[currentGame.turn]}'s Turn"

            if currentGame.timer is not None:
                currentGame.timer.cancel()

            currentGame.timer = asyncio.create_task(self.overtime(gameID))
            colour = (
                discord.Color.blue()
                if currentGame.turn == 1
                else discord.Color.from_rgb(245, 245, 220)
            )

        embed = discord.Embed(
            title=msg,
            description=f"**{currentGame.playerOne}** vs. **{currentGame.playerTwo}**\nuse .move to play",
            color=colour,
        )

        await currentGame.message.edit(embed=embed, content=f"{currentGame.game_board}")

    # -------------------------------------------------------------------------------------------------------#

    @commands.command(aliases=["connect4", "connectfour"])
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def connect(self, ctx, member: discord.Member = None):
        """``connect [@opponent]`` starts a new connect 4 game"""
        game_id = await self.init_game(ctx, member=member, identifier="connect4#")
        if game_id is None:
            return

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

        await self.add_reactions(currentGame.message, self.connectEmojis)

        await self.update_connect_embed(game_id)

    async def update_connect_game(self, game_id, move, payload):
        currentGame = self.games[game_id]
        temp = list(currentGame.grid)
        if payload.user_id == currentGame.current_player.id:
            currentGame.choice = move
            currentGame.update_player()
            if currentGame.grid != temp:
                await self.update_connect_embed(game_id)

    async def update_connect_embed(self, gameID):
        currentGame = self.games[gameID]

        currentGame.draw_board()
        winner, c = currentGame.check_win()
        if not currentGame.run_level:
            if winner is not None:
                if winner == "Tie":
                    colour = self.connectColors[0]
                    msg = "It's a draw!"
                else:
                    colour = self.connectColors[c]
                    msg = f"{currentGame.sprites[c]} {winner} won the game!"

                    if winner.id == currentGame.playerOne.id:
                        loser = currentGame.playerTwo
                    else:
                        loser = currentGame.playerOne

                    await self.update_leaderboards(
                        currentGame.server.id, "connect4", winner.id, loser.id
                    )
            currentGame.timer.cancel()
            await self.close_game(gameID)
        else:

            msg = f"{currentGame.sprites[2] if currentGame.turn == 1 else currentGame.sprites[3]} {currentGame.current_player}'s Turn"

            if currentGame.timer is not None:
                currentGame.timer.cancel()

            currentGame.timer = asyncio.create_task(self.overtime(gameID))
            colour = (
                self.connectColors[2]
                if currentGame.turn == 1
                else self.connectColors[3]
            )

        embed = discord.Embed(
            title=msg, description=f"{currentGame.game_grid}", color=colour,
        )
        embed.set_author(
            name="Connect 4",
            icon_url="https://cdn.discordapp.com/attachments/749779300181606411/774883799347494942/unknown.png",
        )

        embed.add_field(
            name=f"{currentGame.sprites[2]}{currentGame.playerOne}     {currentGame.sprites[3]}{currentGame.playerTwo}",
            value="auto delete in 2 mins",
        )

        await currentGame.message.edit(embed=embed)

    # -------------------------------------------------------------------------------------------------------#

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def filler(self, ctx, member: discord.Member = None):
        """``filler [@opponent]`` starts a new filler game"""
        game_id = await self.init_game(ctx, member=member, identifier="filler#")
        if game_id is None:
            return

        self.games[game_id] = _Filler([8, 7], ctx.author, member, ctx.guild)
        embed = discord.Embed(
            title=f"Filler | {ctx.author} vs. {member}",
            description="Loading... :arrows_counterclockwise:",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/732309032240545883/782327997096263700/unknown.png"
        )
        msg = await ctx.send(embed=embed)

        currentGame = self.games[game_id]
        currentGame.message = msg

        await self.add_reactions(currentGame.message, self.fillerEmojis)
        await self.update_filler_embed(game_id)

    async def update_filler_game(self, game_id, move, payload):
        currentGame = self.games[game_id]

        if move != currentGame.one_pick and move != currentGame.two_pick:
            if currentGame.turn == 1 and payload.user_id == currentGame.playerOne.id:
                currentGame.one_pick = move
                await self.update_filler_embed(game_id)
            elif currentGame.turn == -1 and payload.user_id == currentGame.playerTwo.id:
                currentGame.two_pick = move
                await self.update_filler_embed(game_id)

    async def update_filler_embed(self, gameID):
        currentGame = self.games[gameID]
        currentGame.update_player()
        currentGame.draw_board()
        if not currentGame.run_level:
            winner = currentGame.get_winner()
            if winner != False:
                if winner == currentGame.playerOne:
                    msg = f"{currentGame.sprites[currentGame.one_pick]} {winner} won the game!"
                    colour = self.fillerColors[currentGame.one_pick]
                    loser = currentGame.playerTwo

                elif winner == currentGame.playerTwo:
                    colour = self.fillerColors[currentGame.two_pick]
                    msg = f"{currentGame.sprites[currentGame.two_pick]} {winner} won the game!"
                    loser = currentGame.playerOne

                await self.update_leaderboards(
                    currentGame.server.id, "filler", winner.id, loser.id
                )
            else:
                msg = "It's a draw!"
                colour = discord.Color.default()

            currentGame.timer.cancel()
            await self.close_game(gameID)
        else:
            msg = f"{currentGame.sprites[currentGame.current_colour]} {currentGame.current_player}'s Turn"

            if currentGame.timer is not None:
                currentGame.timer.cancel()

            currentGame.timer = asyncio.create_task(self.overtime(gameID))
            colour = self.fillerColors[currentGame.current_colour]

        embed = discord.Embed(
            title=msg, description=f"{currentGame.game_grid}", color=colour,
        )
        embed.set_author(
            name="Filler",
            icon_url="https://cdn.discordapp.com/attachments/732309032240545883/782327997096263700/unknown.png",
        )
        # embed.set_author(name=f"| Filler |")
        embed.add_field(
            name=f"{currentGame.sprites[currentGame.one_pick]} {currentGame.playerOne}: {currentGame.amountOne}       {currentGame.sprites[currentGame.two_pick]} {currentGame.playerTwo}: {currentGame.amountTwo}",
            value="auto delete in 2 mins",
        )

        await currentGame.message.edit(embed=embed)

    # -------------------------------------------------------------------------------------------------------#
    @commands.command(aliases=["2048"])
    @checks.isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def twenty48(self, ctx):
        """``2048`` starts a new 2048 game."""

        game_id = await self.init_game(ctx, identifier="2048#!")
        if game_id is None:
            return

        self.games[game_id] = TwentyFortyEight(ctx.author, ctx.guild)

        embed = discord.Embed(
            title=f"2048 | {ctx.author}",
            description="Loading... :arrows_counterclockwise:",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/749779300181606411/775809774251540520/2048.png"
        )
        msg = await ctx.send(embed=embed, content=f"{ctx.author}'s Game",)
        # await ctx.send(f"{ctx.author.mention}'s Game:")

        currentGame = self.games[game_id]
        currentGame.message = msg

        await self.add_reactions(currentGame.message, self.twenty48Emojis)
        await self.update_2048_embed(game_id)

    async def update_2048_game(self, game_id, move, payload):

        currentGame = self.games[game_id]
        currentGame.move = move
        temp = currentGame.grid
        currentGame.update_game()
        if currentGame.game_end():
            if currentGame.grid != temp:
                currentGame.moves += 1
                currentGame.spawn_random()

        await self.update_2048_embed(game_id)

    async def update_2048_embed(self, gameID):
        currentGame = self.games[gameID]
        currentGame.draw_board()

        if not currentGame.game_end():
            currentGame.timer.cancel()
            await self.close_game(gameID)

            msg = f"Game Over {currentGame.user}\nScore: {currentGame.score} | Moves: {currentGame.moves}"
        else:
            msg = f"Score: {currentGame.score} | Moves: {currentGame.moves}"

            #  await currentGame.message.edit(content=)
        embed = discord.Embed(
            title=msg,
            description=f"auto delete in 2 mins",
            color=currentGame.user.color,
        )
        embed.set_author(name=f"{currentGame.user}'s Game:",)

        await currentGame.message.edit(embed=embed, content=f"{currentGame.game_grid}")

        if currentGame.timer is not None:
            currentGame.timer.cancel()

        currentGame.timer = asyncio.create_task(
            self.overtime(
                gameID,
                f"{currentGame.user} ended with a score of {currentGame.score} in {currentGame.moves} moves.",
            )
        )

    # -------------------------------------------------------------------------------------------------------#
    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.guild)
    @commands.has_permissions(embed_links=True)
    async def sokoban(self, ctx):
        """``sokoban`` starts a new sokoban game"""

        game_id = await self.init_game(ctx, identifier="sokoban#!")
        if game_id is None:
            return
        # max [9, 7]
        self.games[game_id] = Soko_ban([5, 3], ctx.author, ctx.guild)
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

        await self.add_reactions(currentGame.message, self.sokobanEmojis)
        await self.update_sokoban_embed(game_id)

    async def update_sokoban_game(self, game_id, move, payload):
        currentGame = self.games[game_id]
        currentGame.move = move
        if move == "theme":
            currentGame.theme_num += 1
            if currentGame.theme_num >= len(self.themes):
                currentGame.theme_num = 0

            currentGame.sprites = self.themes[currentGame.theme_num]

        await self.update_sokoban_embed(game_id)

    async def update_sokoban_embed(self, gameID):
        currentGame = self.games[gameID]
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
            value="auto delete in 2 mins",
        )
        await currentGame.message.edit(embed=embed)

        if currentGame.timer is not None:
            currentGame.timer.cancel()

        currentGame.timer = asyncio.create_task(
            self.overtime(
                gameID, f"{currentGame.user} made it to level {currentGame.level}!"
            )
        )


def setup(bot):
    bot.add_cog(Games(bot))
