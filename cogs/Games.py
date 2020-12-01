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

blacklist = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/blacklist.json"
    )
)["commandblacklist"][f"{os.path.basename(__file__)[:-3]}"]


def isAllowedCommand():
    async def predicate(ctx):
        return ctx.guild.id not in blacklist

    return commands.check(predicate)


class Games(commands.Cog):
    """Play Games, all games auto delete if theres no input for 5 minutes"""

    def __init__(self, bot):
        self.bot = bot
        self.games_log = {}
        self.games = {}
        self.keys = {}

        self.info = json.load(
            open(
                f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/sokoban.json"
            )
        )
        self.chessEmojis = {"none": "none"}

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
            # "update_chess_game": self.update_chess_game,
            # "update_chess_embed": self.update_chess_embed,
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

    @commands.command()
    @commands.is_owner()
    async def gamelog(self, ctx):
        log = "\n".join([f"{self.games_log[k]} | {k}" for k in self.games_log])
        await ctx.send(f"```{len(self.games_log)} Games:\n{log}```")

    async def overtime(self, gameID, extras="No Winner"):
        self.games_log[f"ID:{gameID}"] = f"{gameID[: gameID.index('#')]}"

        await asyncio.sleep(300)
        await self.delete_game(gameID, extras)

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
                        gameType = game_id[: game_id.index("#")]

                        if str(payload.emoji) in self.gameCalls[f"{gameType}Emojis"]:
                            move = self.gameCalls[f"{gameType}Emojis"][
                                str(payload.emoji)
                            ]
                            await self.gameCalls[f"update_{gameType}_game"](
                                game_id, move, payload
                            )

                        else:
                            if str(payload.emoji) == "❌":
                                await self.delete_game(game_id, "Game Was Deleted")
                                return

                        await currentGame.message.remove_reaction(
                            member=payload.member, emoji=payload.emoji
                        )

    async def delete_game(self, gameID, extras="Timed Out"):
        gameType = gameID[: gameID.index("#")]
        try:
            currentGame = self.games[gameID]
        except KeyError:
            return

        embed = discord.Embed(title=gameType.capitalize())
        embed.set_author(name=extras)
        embed.set_footer(text="Game was deleted.")
        self.games.pop(gameID)
        if "!" not in gameID:
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))
            content = None
        else:
            self.keys.pop(str(currentGame.server.id) + str(currentGame.user.id))
            content = " "

        try:
            await currentGame.message.clear_reactions()
            await currentGame.message.edit(embed=embed, content=content)
        except discord.errors.NotFound:
            print(f"Could not delete {gameType} game!")

        currentGame.timer.cancel()

    async def add_reactions(self, msg, emojis):
        for emoji in emojis:
            await msg.add_reaction(emoji)
        await msg.add_reaction("❌")

    # -------------------------------------------------------------------------------------------------------#
    @commands.command(aliases=["2048"])
    @isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def twenty48(self, ctx):
        """``2048`` starts a new 2048 game."""
        if str(ctx.guild.id) + str(ctx.author.id) in self.keys:
            await ctx.send("You are currently in a game!")
            return

        self.keys[str(ctx.guild.id) + str(ctx.author.id)] = (
            "2048#!" + str(ctx.guild.id) + str(ctx.author.id)
        )
        game_id = self.keys[str(ctx.guild.id) + str(ctx.author.id)]

        if game_id in self.games:
            await self.games[game_id].message.delete()

        # max [9, 7]
        self.games[game_id] = TwentyFortyEight(ctx.author, ctx.guild)

        # msg = await ctx.send(
        #     embed=discord.Embed(title=f"2048 | {ctx.author}"),
        #     content=f"{ctx.author.mention} Loading... :arrows_counterclockwise:",
        # )

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
            self.games.pop(gameID)
            self.keys.pop(str(currentGame.server.id) + str(currentGame.user.id))
            await currentGame.message.clear_reactions()

            msg = f"Game Over {currentGame.user}\nScore: {currentGame.score} | Moves: {currentGame.moves}"
        else:
            msg = f"Score: {currentGame.score} | Moves: {currentGame.moves}"

            #  await currentGame.message.edit(content=)
        embed = discord.Embed(
            title=msg,
            description=f"auto delete in 5 mins",
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
    @isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.has_permissions(embed_links=True)
    async def sokoban(self, ctx):
        """``sokoban`` starts a new sokoban game"""

        if str(ctx.guild.id) + str(ctx.author.id) in self.keys:
            await ctx.send("You are currently in a game!")
            return

        self.keys[str(ctx.guild.id) + str(ctx.author.id)] = (
            "sokoban#!" + str(ctx.guild.id) + str(ctx.author.id)
        )
        game_id = self.keys[str(ctx.guild.id) + str(ctx.author.id)]

        if game_id in self.games:
            await self.games[game_id].message.delete()

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
            value="auto delete in 5 mins",
        )
        await currentGame.message.edit(embed=embed)

        if currentGame.timer is not None:
            currentGame.timer.cancel()

        currentGame.timer = asyncio.create_task(
            self.overtime(
                gameID, f"{currentGame.user} made it to level {currentGame.level}!"
            )
        )

    # -------------------------------------------------------------------------------------------------------#

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def chess(self, ctx, member: discord.Member = None):
        """``chess [@opponent]`` starts a new chess game. Use .move to play `BETA`"""
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
            "chess#" + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
        )

        self.keys[str(ctx.guild.id) + str(member.id)] = (
            "chess#" + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
        )

        game_id = self.keys[str(ctx.guild.id) + str(ctx.author.id)]

        if game_id in self.games:
            await self.games[game_id].message.delete()

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
    @isAllowedCommand()
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
            msg = currentGame.update_game()
            if msg is not None:
                invalid_move = await ctx.send(msg)
            else:
                await self.update_chess_embed(game_id)
        else:
            invalid_move = await ctx.send("It's not your turn!")

        if invalid_move is not None:
            await invalid_move.add_reaction("<:trash:783097450461397052>")

        await ctx.message.delete()

    async def update_chess_embed(self, gameID, delete=False):
        currentGame = self.games[gameID]

        currentGame.draw_board()
        currentGame.check_end()
        if not currentGame.run_game:
            if currentGame.winner == "DRAW":
                msg = "Draw"
            elif currentGame.winner == -1:
                msg = f"<:W_:776325516118065152>{currentGame.current_player[-1]} won by {currentGame.reason}"
                colour = discord.Color.from_rgb(245, 245, 220)

            elif currentGame.winner == 1:
                msg = f"<:B_:776325516096569384>{currentGame.current_player[1]} won by {currentGame.reason}"
                colour = discord.Color.blue()

            currentGame.timer.cancel()
            self.games.pop(gameID)
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))
            await currentGame.message.clear_reactions()
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
        # embed.set_author(
        #     name="Chess",
        #     icon_url="https://cdn.discordapp.com/attachments/749779300181606411/774883799347494942/unknown.png",
        # )

        # embed.add_field(
        #     name=,
        #     value="auto delete in 5 mins",
        # )

        await currentGame.message.edit(embed=embed, content=f"{currentGame.game_board}")

    # -------------------------------------------------------------------------------------------------------#

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def connect(self, ctx, member: discord.Member = None):
        """``connect [@opponent]`` starts a new connect 4 game"""
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
            "connect4#" + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
        )

        self.keys[str(ctx.guild.id) + str(member.id)] = (
            "connect4#" + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
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

    async def update_connect_embed(self, gameID, delete=False):
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

            currentGame.timer.cancel()
            self.games.pop(gameID)
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))
            await currentGame.message.clear_reactions()
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
            value="auto delete in 5 mins",
        )

        await currentGame.message.edit(embed=embed)

    # -------------------------------------------------------------------------------------------------------#

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def filler(self, ctx, member: discord.Member = None):
        """``filler [@opponent]`` starts a new filler game"""
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
            "filler#" + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
        )

        self.keys[str(ctx.guild.id) + str(member.id)] = (
            "filler#" + str(ctx.guild.id) + str(ctx.author.id) + str(member.id)
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
                elif winner == currentGame.playerTwo:
                    colour = self.fillerColors[currentGame.two_pick]
                    msg = f"{currentGame.sprites[currentGame.two_pick]} {winner} won the game!"
            else:
                msg = "It's a draw!"
                colour = discord.Color.default()

            currentGame.timer.cancel()
            self.games.pop(gameID)
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
            self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))
            await currentGame.message.clear_reactions()
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
            value="auto delete in 5 mins",
        )

        await currentGame.message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))
