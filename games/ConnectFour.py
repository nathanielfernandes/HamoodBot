import discord
from games.DefaultGame import DefaultGame


class ConnectFour(DefaultGame):
    def __init__(
        self,
        ctx,
        playerTwo=None,
        wager: int = 0,
    ):
        super().__init__(
            ctx=ctx,
            playerTwo=playerTwo,
            wager=wager,
            game_name="connect4",
            thumbnail="https://cdn.discordapp.com/attachments/749779300181606411/774883799347494942/unknown.png",
            reactions={
                "<:one:823355865481871390>": 0,
                "<:two:823355865380945951>": 1,
                "<:three:823355865376751638>": 2,
                "<:four:823355865348177930>": 3,
                "<:five:823355865138331649>": 4,
                "<:six:823355865247383594>": 5,
                "<:seven:823355865431801856>": 6,
            },
        )

        self.emojis = [
            "<:empty:823351307279663145>",
            "<:redinside:823347539813335071>",
            "<:yellowinside:823347539724992522>",
            "<:leftside:823351703402578001>",
            "<:rightside:823351703842979880>",
            "<:one:823355865481871390>",
            "<:two:823355865380945951>",
            "<:three:823355865376751638>",
            "<:four:823355865348177930>",
            "<:five:823355865138331649>",
            "<:six:823355865247383594>",
            "<:seven:823355865431801856>",
        ]
        self.pieces = {
            self.playerOne.id: [
                "<:redcircle:823347539460882453>",
                discord.Color.red(),
                1,
            ],
            self.playerTwo.id: [
                "<:yellowcircle:823347539495092226>",
                discord.Color.gold(),
                2,
            ],
        }

    async def game_start(self):
        self.grid = [[0] * 7 for i in range(6)]
        await self.update_message(embed=self.create_embed())

    async def update_game(self, member, move, emoji):
        if member == self.current_turn:
            if self.drop_piece(move, self.pieces[member.id][2]):
                self.swap_turns()
                p = self.check_win()
                winner, loser, tie = None, None, False
                if p != 0:
                    if p == 1:
                        winner = self.playerOne
                        loser = self.playerTwo
                    elif p == 2:
                        winner = self.playerTwo
                        loser = self.playerTwo
                    elif p == -1:
                        tie = True
                    await self.end_game(winner=winner, loser=loser, tie=tie)
                await self.update_message(
                    embed=self.create_embed(winner=winner, tie=tie)
                )

    def check_win(self):
        full = True
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != 0:
                    d, r, dr, ur = 1, 1, 1, 1
                    while (0 <= y + d <= 5) and (
                        self.grid[y + d][x] == self.grid[y][x]
                    ):
                        d += 1
                        if d >= 4:
                            return self.grid[y][x]
                    while (0 <= x + r <= 6) and (
                        self.grid[y][x + r] == self.grid[y][x]
                    ):
                        r += 1
                        if r >= 4:
                            return self.grid[y][x]
                    while (0 <= y + dr <= 5 and 0 <= x + dr <= 6) and (
                        self.grid[y + dr][x + dr] == self.grid[y][x]
                    ):
                        dr += 1
                        if dr >= 4:
                            return self.grid[y][x]
                    while (0 <= y - ur <= 5 and 0 <= x - ur <= 6) and (
                        self.grid[y - ur][x - ur] == self.grid[y][x]
                    ):
                        ur -= 1
                        if ur >= 4:
                            return self.grid[y][x]
                else:
                    full = False
        return 0 if not full else -1

    def drop_piece(self, x: int, p: int):
        col = [list(row) for row in zip(*self.grid)][x]
        try:
            y = len(col) - 1 - col[::-1].index(0)
            self.grid[y][x] = p
            return True
        except ValueError:
            return False

    def create_embed(self, winner=None, tie=False):
        if tie:
            color = discord.Color.orange()
            title = "It's a draw!"
        elif winner is not None:
            color = self.pieces[winner.id][1]
            title = f"{self.pieces[winner.id][0]} **{winner}** won the game!"
        else:
            color = self.pieces[self.current_turn.id][1]
            title = f"{self.pieces[self.current_turn.id][0]} {self.current_turn}'s Turn"

        embed = discord.Embed(
            title=title, description=f"{self.grid_str()}", color=color
        )

        value = f"wager: {self.cash(self.wager)}" if self.wager > 0 else "\u200b"
        embed.add_field(
            name=f"{self.pieces[self.playerOne.id][0]}{self.playerOne}     {self.pieces[self.playerTwo.id][0]}{self.playerTwo}",
            value=value,
        )
        embed.set_author(name=self.game_name.title(), icon_url=self.thumbnail)

        return embed

    def grid_str(self):
        string = ""
        for row in self.grid:
            string += (
                self.emojis[3]
                + "".join([self.emojis[i] for i in row])
                + self.emojis[4]
                + "\n"
            )
        string += self.emojis[3] + "".join(self.emojis[5:]) + self.emojis[4]

        return string
