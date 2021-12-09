import asyncio
import discord


class DefaultGame:
    def __init__(
        self,
        game_name: str,
        thumbnail: str,
        ctx,
        playerTwo=None,
        reactions: dict = {},
        solo: bool = False,
        turn_based: bool = True,
        extra_info: str = "",
        wager: int = 0,
    ):

        self.game_name = game_name
        self.extra_info = extra_info
        self.thumbnail = thumbnail

        self.ctx = ctx
        self.bot = ctx.bot
        self.Hamood = self.bot.Hamood
        self.games = self.Hamood.active_games

        self.prefix = self.Hamood.find_prefix(ctx.guild.id)
        self.guild_id = ctx.guild.id
        self.playerOne = ctx.author

        self.current_turn = self.playerOne

        self.game_id_1 = str(self.guild_id) + str(self.playerOne.id)

        if not solo:
            self.playerTwo = playerTwo
            self.game_id_2 = str(self.guild_id) + str(playerTwo.id)

        self.game_started = False
        self.solo = solo
        self.turn_based = turn_based

        if turn_based:
            self.current_turn = self.playerTwo
            self.off_turn = self.playerOne

        self.reactions = reactions

        self.join_emoji = "✅"
        self.leave_emoji = "🚪"

        self.cash = lambda n: f"[⌬ {n:,}](https://top.gg/bot/699510311018823680)"
        self.wager = wager

        self.timer = asyncio.create_task(self.game_timer())

        self.gameover = False

    async def load_game(self):
        """Called automatically once a player accepts and invite or a solo game is started.\n
        Adds all the reactions required for the game and deducts the wager from the joined
        player if the game is not solo.\n
        Calls the self.game_start() method which needs to be implemented by the game.
        """
        half = str(self.playerOne)
        if not self.solo:
            half += f" vs. {self.playerTwo}"

        embed = discord.Embed(
            title=f"{self.game_name.title()} | {half}",
            description="Loading... <a:loading:856302946274246697>",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=self.thumbnail)
        if self.solo:
            self.message = await self.ctx.send(embed=embed)
        else:
            if self.wager > 0:
                playerTwoBal = await self.Hamood.Currency.get_currency(
                    self.guild_id, self.playerTwo.id
                )
                if playerTwoBal["bank"] >= self.wager:
                    await self.Hamood.Currency.update_bank(
                        self.guild_id, self.playerTwo.id, -1 * self.wager
                    )
                else:
                    await self.message.clear_reactions()
                    return await self.message.edit(
                        content=f"`{self.playerTwo}` does not have the bank balance to bet `⌬ {self.wager:,}`",
                        embed=None,
                    )
            await self.message.clear_reactions()
            await self.message.edit(embed=embed)

        finished = await self.add_reactions()
        if finished:
            self.game_started = True
            await self.game_start()

    async def create_invite(self):
        """Called automatically if the game is not a solo game.\n
        Creates an invite message for another player to accept.
        """
        wager_msg = f"\n**Wager:** {self.cash(self.wager)}" if self.wager > 0 else ""
        embed = discord.Embed(
            title=f"{self.game_name.title()}",
            description=f"{self.playerOne.mention} wants to start a game of **{self.game_name.title()}** with {self.playerTwo.mention}\n{wager_msg}\n{self.extra_info}\nClick {self.join_emoji} to join the game or {self.leave_emoji} to leave.",
            color=self.playerOne.color,
        )
        embed.set_thumbnail(url=self.thumbnail)
        embed.set_footer(text="Games are deleted after 5 minutes of inactivity.")
        self.message = await self.ctx.send(embed=embed)
        await self.message.add_reaction(self.join_emoji)
        await self.message.add_reaction(self.leave_emoji)

    async def setup_game(self):
        """Sets up the game, checking for duplicate games and insufficient funds.\n
        Creates an invite if the game is not solo, otherwise just loads the game.
        """

        if self.game_id_1 in self.games:
            await self.ctx.send(
                f"You are currently in a game! Use `{self.prefix}leavegame` to leave ur current game."
            )
            return False

        if not self.solo:
            if self.game_id_2 in self.games:
                await self.ctx.send(
                    f"`{self.playerTwo}` is currently in a game or has a pending invite."
                )
                return False
            elif (
                self.playerTwo is None
                or self.playerTwo.bot
                or self.playerTwo == self.playerOne
            ):
                await self.ctx.send("You haven't tagged a valid member.")
                return False

        if self.wager > 0:
            playerOneBal = await self.Hamood.Currency.get_currency(
                self.guild_id, self.playerOne.id
            )

            if playerOneBal is None or playerOneBal["bank"] < self.wager:
                await self.ctx.send(
                    f"You do not have the bank balance to bet `⌬ {self.wager:,}`"
                )
                return False

            if not solo:
                playerTwoBal = await self.Hamood.Currency.get_currency(
                    self.guild_id, self.playerTwo.id
                )

                if playerTwoBal is None or playerTwoBal["bank"] < self.wager:
                    await self.ctx.send(
                        f"`{self.playerTwo}` does not have the bank balance to bet `⌬ {self.wager:,}`"
                    )
                    return False

            await self.Hamood.Currency.update_bank(
                self.guild_id, self.playerOne.id, -1 * self.wager
            )

        self.games[self.game_id_1] = self
        if not self.solo:
            self.games[self.game_id_2] = self
            await self.create_invite()
        else:
            await self.load_game()

        return True

    async def update_leaderboards(self, winner=None, loser=None, tie=False):
        """Updates the leaderboard database given a tie, winner or a loser or both.\n
        Handles the win/loss counter as well has wager winnings/losings.
        """
        if tie:
            if self.wager > 0:
                await self.Hamood.Currency.update_wallet(
                    self.guild_id, self.playerOne.id, self.wager
                )
                if not self.solo:
                    await self.Hamood.Currency.update_wallet(
                        self.guild_id, self.playerTwo.id, self.wager
                    )
        else:
            await self.Hamood.Leaderboards.add_leaderboard(self.guild_id)
            if winner:
                if self.wager > 0:
                    await self.Hamood.Currency.update_wallet(
                        self.guild_id, winner.id, self.wager * 2
                    )

                await self.Hamood.Leaderboards.add_member(self.guild_id, winner.id)
                await self.Hamood.Leaderboards.add_game(
                    self.guild_id, winner.id, self.game_name
                )
                await self.Hamood.Leaderboards.incr_game_won(
                    self.guild_id, winner.id, self.game_name
                )
            if loser:
                await self.Hamood.Leaderboards.add_member(self.guild_id, loser.id)
                await self.Hamood.Leaderboards.add_game(
                    self.guild_id, loser.id, self.game_name
                )
                await self.Hamood.Leaderboards.incr_game_lost(
                    self.guild_id, loser.id, self.game_name
                )

    async def clear_game(self):
        """Removes a game from the existsing games dict, deleting player keys.\n
        Clears all the reactions from a game too.
        """
        try:
            del self.games[self.game_id_1]
            if not self.solo:
                del self.games[self.game_id_2]
        except KeyError:
            pass

        try:
            await self.message.clear_reactions()
        except Exception:
            pass

        self.gameover = True

    async def end_game(self, winner=None, loser=None, tie=False):
        """Ends the game without removing the existing messsage.\n
        Should be used when a win, loss, or tie occurs.
        """
        await self.clear_game()
        await self.update_leaderboards(winner, loser, tie)
        await self.kill_timer()

    async def delete_game(self, member=None, custom_msg=""):
        """Called automatically when a user decides to leave a game.\n
        Should only be used when there has been a player forfiet.\n
        Use self.end_game() if the game just needs to be ended.
        """
        await self.clear_game()
        if not self.solo:
            if self.game_started:
                if member is None:
                    if self.turn_based:
                        winner = self.off_turn
                        loser = self.current_turn
                        custom_msg = f"{winner} won by default!"
                    else:
                        winner = None
                        loser = None
                        custom_msg = f"Game Timed Out"
                else:
                    temp = [self.playerOne, self.playerTwo]
                    temp.remove(member)
                    winner = temp[0]
                    loser = member
                    custom_msg = f"{winner} won by default!"

                await self.update_leaderboards(winner, loser)

            else:
                if self.wager > 0:
                    await self.Hamood.Currency.update_wallet(
                        self.guild_id, self.playerOne.id, self.wager
                    )
                custom_msg = "No Winner"

        else:
            if self.game_started:
                await self.update_leaderboards(loser=self.playerOne)
                custom_msg = f"{self.playerOne} forfeited!"
            else:
                if self.wager > 0:
                    await self.Hamood.Currency.update_wallet(
                        self.guild_id, self.playerOne.id, self.wager
                    )
                custom_msg = f"Game Cancelled"

        embed = discord.Embed(
            title=self.game_name.title(),
            description=f"\n**Wager:** {self.cash(self.wager)}"
            if self.wager > 0
            else "",
        )
        embed.set_author(name=custom_msg)
        embed.set_footer(text="Game was ended.")

        try:
            await self.message.edit(embed=embed, content=" ")
        except discord.errors.NotFound:
            pass

        self.message = None

        await self.kill_timer()

    async def kill_timer(self):
        try:
            self.timer.cancel()
        except Exception:
            pass

    async def reset_timer(self):
        """Resets the 5 minute game timer.\n
        Called automatically, but can be called if necessary.
        """
        try:
            self.timer.cancel()
            self.timer = asyncio.create_task(self.game_timer())
        except Exception:
            pass

    async def game_timer(self):
        """Automatic game deletetion timer.
        Called automatically and should not be used.
        """
        await asyncio.sleep(120)
        await self.delete_game()

    async def on_reaction(self, payload):
        """Called on every reaction event to the game.\n
        Calls self.update_game with the 'move' the player moved.\n
        Handles leaving games automatically.
        """
        if payload.message_id == self.message.id and (
            payload.member == self.playerOne
            or (not self.solo and payload.member == self.playerTwo)
        ):
            if self.game_started and str(payload.emoji) in self.reactions:
                await self.update_game(
                    member=payload.member,
                    move=self.reactions[str(payload.emoji)],
                    emoji=str(payload.emoji),
                )
                await self.message.remove_reaction(
                    member=payload.member, emoji=str(payload.emoji)
                )
            elif (
                str(payload.emoji) == self.join_emoji
                and payload.member == self.playerTwo
            ):
                await self.load_game()
            elif str(payload.emoji) == self.leave_emoji:
                await self.delete_game(
                    payload.member, custom_msg=f"{payload.member.name} closed the game"
                )

    async def add_reactions(self):
        """Adds all the reactions in self.reactions to the game message.\n
        Called automatically.
        """
        if self.reactions is not None:
            for emoji in self.reactions:
                await self.message.add_reaction(emoji)
        await self.message.add_reaction(self.leave_emoji)
        return True

    async def update_message(self, embed=None, content=None):
        """Resets the game timer and edits the game message with the embed and content specified."""
        if not self.gameover:
            await self.reset_timer()
        await self.message.edit(embed=embed, content=content)

    def swap_turns(self):
        """Swaps self.current_turn and self.off_turn.\n
        Must be used if the game is turn based.\n
        Should only be used when the game is not solo.
        """
        self.current_turn = (
            self.playerOne if self.current_turn == self.playerTwo else self.playerTwo
        )
        self.off_turn = (
            self.playerOne if self.off_turn == self.playerTwo else self.playerTwo
        )

    # TODO
    async def update_game(self, member, move, emoji):
        """interface method\n
        Called on a player reaction.\n
        Needs to be implemented by the game.
        """
        pass

    # TODO
    async def game_start(self):
        """interface method\n
        Called on a player reaction.\n
        Needs to be implemented by the game.
        """
        pass
