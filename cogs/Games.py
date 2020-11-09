import asyncio
import discord
from discord.ext import commands

from modules.filler_functions import _Filler
from modules.connect4_functions import Connect_Four


class Games(commands.Cog):
    """Play Games, all games auto delete if theres no input for 5 minutes"""

    def __init__(self, bot):
        self.bot = bot

        self.games = {}
        self.keys = {}

        self.fillerEmojis = [
            "\U0001F7E5",
            "\U0001F7E7",
            "\U0001F7E8",
            "\U0001F7E9",
            "\U0001F7E6",
            "\U0001F7EA",
        ]
        self.fillerColors = [
            discord.Color.red(),
            discord.Color.orange(),
            discord.Color.gold(),
            discord.Color.green(),
            discord.Color.blue(),
            discord.Color.purple(),
        ]

        self.connectEmojis = [
            "\U0001F550",
            "\U0001F551",
            "\U0001F552",
            "\U0001F553",
            "\U0001F554",
            "\U0001F555",
            "\U0001F556",
        ]
        self.connectColors = [
            discord.Color.blue(),
            discord.Color.orange(),
            discord.Color.red(),
            discord.Color.gold(),
        ]

        self.gameCalls = {
            "update_connect4_game": self.update_connect_game,
            "update_connect4_embed": self.update_connect_embed,
            "connect4Emojis": self.connectEmojis,
            "update_filler_game": self.update_filler_game,
            "update_filler_embed": self.update_filler_embed,
            "fillerEmojis": self.fillerEmojis,
        }

    async def overtime(self, gameID):
        await asyncio.sleep(300)
        await self.delete_game(gameID)

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
                            for emoji in self.gameCalls[f"{gameType}Emojis"]:
                                if str(payload.emoji) == emoji:
                                    await self.gameCalls[f"update_{gameType}_game"](
                                        game_id, emoji, payload
                                    )
                        else:
                            if str(payload.emoji) == "❌":
                                await self.delete_game(game_id)
                                return

                        await currentGame.message.remove_reaction(
                            member=payload.member, emoji=payload.emoji
                        )

    async def delete_game(self, gameID):
        gameType = gameID[: gameID.index("#")]
        currentGame = self.games[gameID]
        embed = discord.Embed(title=gameType.capitalize())
        embed.set_author(name="No Winner")
        embed.set_footer(text="Game was deleted.")
        self.games.pop(gameID)
        self.keys.pop(str(currentGame.server.id) + str(currentGame.playerOne.id))
        self.keys.pop(str(currentGame.server.id) + str(currentGame.playerTwo.id))

        try:
            await currentGame.message.clear_reactions()
            await currentGame.message.edit(embed=embed)
        except discord.errors.NotFound:
            print(f"Could not delete {gameType} game!")

        currentGame.timer.cancel()

    # -------------------------------------------------------------------------------------------------------#

    @commands.command()
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

        for emoji in self.connectEmojis:
            await currentGame.message.add_reaction(emoji)
        await currentGame.message.add_reaction("❌")

        await self.update_connect_embed(game_id)

    async def update_connect_game(self, game_id, emoji, payload):
        currentGame = self.games[game_id]
        temp = list(currentGame.grid)
        if payload.user_id == currentGame.current_player.id:
            currentGame.choice = self.connectEmojis.index(emoji) + 1
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

            if currentGame.timer != None:
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
            url="https://cdn.discordapp.com/attachments/699770186227646465/744962953006153738/unknown.png"
        )
        msg = await ctx.send(embed=embed)

        currentGame = self.games[game_id]
        currentGame.message = msg

        for emoji in self.fillerEmojis:
            await currentGame.message.add_reaction(emoji)
        await currentGame.message.add_reaction("❌")

        await self.update_filler_embed(game_id)

    async def update_filler_game(self, game_id, emoji, payload):
        currentGame = self.games[game_id]
        pick = self.fillerEmojis.index(emoji)

        if pick != currentGame.one_pick and pick != currentGame.two_pick:
            if currentGame.turn == 1 and payload.user_id == currentGame.playerOne.id:
                currentGame.one_pick = pick
                await self.update_filler_embed(game_id)
            elif currentGame.turn == -1 and payload.user_id == currentGame.playerTwo.id:
                currentGame.two_pick = pick
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

            if currentGame.timer != None:
                currentGame.timer.cancel()

            currentGame.timer = asyncio.create_task(self.overtime(gameID))
            colour = self.fillerColors[currentGame.current_colour]
        embed = discord.Embed(
            title=msg, description=f"{currentGame.game_grid}", color=colour,
        )
        embed.set_author(
            name="Filler",
            icon_url="https://cdn.discordapp.com/attachments/699770186227646465/744962953006153738/unknown.png",
        )
        # embed.set_author(name=f"| Filler |")
        embed.add_field(
            name=f"{currentGame.sprites[currentGame.one_pick]} {currentGame.playerOne}: {currentGame.amountOne}       {currentGame.sprites[currentGame.two_pick]} {currentGame.playerTwo}: {currentGame.amountTwo}",
            value="auto delete in 5 mins",
        )

        await currentGame.message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))
