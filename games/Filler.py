import random
import discord
from games.DefaultGame import DefaultGame


class Filler(DefaultGame):
    def __init__(
        self, ctx, bot, playerTwo=None, wager: int = 0,
    ):
        super().__init__(
            ctx=ctx,
            bot=bot,
            playerTwo=playerTwo,
            wager=wager,
            game_name="filler",
            thumbnail="https://cdn.discordapp.com/attachments/732309032240545883/782327997096263700/unknown.png",
            reactions={
                "<:red:782108442998997003>": 0,
                "<:blue:782108442851803158>": 1,
                "<:green:782108443418689536>": 2,
                "<:yellow:782108443225751552>": 3,
                "<:purple:782108443284733962>": 4,
                "<:black:782108442835812374>": 5,
            },
        )

        self.emojis = [
            "<:red:782108442998997003>",
            "<:blue:782108442851803158>",
            "<:green:782108443418689536>",
            "<:yellow:782108443225751552>",
            "<:purple:782108443284733962>",
            "<:black:782108442835812374>",
        ]

        self.animated_emojis = [
            "<a:redg:782108443238465556>",
            "<a:blueg:782108443045134387>",
            "<a:greeng:782108443184070696>",
            "<a:yellowg:782108443179876352>",
            "<a:purpleg:782108443296530432>",
            "<a:blackg:782108443124695092>",
        ]

        self.colors = [
            discord.Color.from_rgb(229, 43, 92),
            discord.Color.from_rgb(56, 158, 220),
            discord.Color.from_rgb(166, 227, 90),
            discord.Color.from_rgb(251, 235, 62),
            discord.Color.from_rgb(115, 79, 166),
            discord.Color.from_rgb(64, 64, 64),
        ]

    async def game_start(self):
        self.grid = [[-1] * 8 for i in range(7)]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                r = list(range(6))
                r.remove(self.grid[y][x - 1]) if self.grid[y][x - 1] in r else None
                r.remove(self.grid[y - 1][x]) if self.grid[y - 1][x] in r else None
                if (y, x) == (6, 0):
                    r.remove(self.grid[0][7]) if self.grid[0][7] in r else None
                self.grid[y][x] = random.choice(r)

        self.players = {
            self.playerOne.id: {
                "i": self.grid[6][0],
                "c": self.colors[self.grid[6][0]],
                "l": [(6, 0)],
                "t": 1,
            },
            self.playerTwo.id: {
                "i": self.grid[0][7],
                "c": self.colors[self.grid[0][7]],
                "l": [(0, 7)],
                "t": 1,
            },
        }
        await self.update_message(embed=self.create_embed())

    async def update_game(self, member, move, emoji):
        if member == self.current_turn:
            if self.switch_color(member, move):
                self.swap_turns()
                result = self.check_win()
                winner, loser, tie = None, None, False
                if result != 0:
                    if result == 1:
                        tie = True
                    else:
                        winner, loser = result
                    await self.end_game(winner=winner, loser=loser, tie=tie)
                await self.update_message(
                    embed=self.create_embed(winner=winner, tie=tie)
                )

    def check_win(self):
        p1t = self.players[self.playerOne.id]["t"]
        p2t = self.players[self.playerTwo.id]["t"]
        if p1t + p2t == 56:
            if p1t > p2t:
                return self.playerOne, self.playerTwo
            elif p1t < p2t:
                return self.playerTwo, self.playerOne
            else:
                return 1
        return 0

    def switch_color(self, member, move):
        if (move != self.players[self.playerOne.id]["i"]) and (
            move != self.players[self.playerTwo.id]["i"]
        ):
            for y, x in self.players[member.id]["l"]:
                self.grid[y][x] = move
                if y - 1 >= 0:
                    if self.grid[y - 1][x] == move:
                        self.players[member.id]["l"].append((y - 1, x)) if (
                            y - 1,
                            x,
                        ) not in self.players[member.id]["l"] else None

                if y + 1 < len(self.grid):
                    if self.grid[y + 1][x] == move:
                        self.players[member.id]["l"].append((y + 1, x)) if (
                            y + 1,
                            x,
                        ) not in self.players[member.id]["l"] else None

                if x - 1 >= 0:
                    if self.grid[y][x - 1] == move:
                        self.players[member.id]["l"].append((y, x - 1)) if (
                            y,
                            x - 1,
                        ) not in self.players[member.id]["l"] else None

                if x + 1 < len(self.grid[0]):
                    if self.grid[y][x + 1] == move:
                        self.players[member.id]["l"].append((y, x + 1)) if (
                            y,
                            x + 1,
                        ) not in self.players[member.id]["l"] else None

                for y, x in self.players[member.id]["l"]:
                    self.grid[y][x] = move

            self.players[member.id]["l"] = list(
                dict.fromkeys(self.players[member.id]["l"])
            )
            self.players[member.id]["t"] = len(self.players[member.id]["l"])
            self.players[member.id]["i"] = move
            self.players[member.id]["c"] = self.colors[move]
            return True
        return False

    def create_embed(self, winner=None, tie=False):
        end = False
        if tie:
            color = discord.Color.from_rgb(245, 245, 245)
            title = "It's a draw!"
            end = True
        elif winner is not None:
            color = self.players[winner.id]["c"]
            title = f"{self.emojis[self.players[winner.id]['i']]} **{winner}** won the game!"
            end = True
        else:
            color = self.players[self.current_turn.id]["c"]
            title = f"{self.emojis[self.players[self.current_turn.id]['i']]} {self.current_turn}'s Turn"

        embed = discord.Embed(
            title=title, description=f"{self.grid_str(end)}", color=color
        )

        value = f"wager: {self.cash(self.wager)}" if self.wager > 0 else "."
        embed.add_field(
            name=f"{self.emojis[self.players[self.playerOne.id]['i']]} {self.playerOne}: {self.players[self.playerOne.id]['t']}    {self.emojis[self.players[self.playerTwo.id]['i']]} {self.playerTwo}: {self.players[self.playerTwo.id]['t']}",
            value=value,
        )
        embed.set_author(name=self.game_name.title(), icon_url=self.thumbnail)

        return embed

    def grid_str(self, end=False):
        return "\n".join(
            [
                "".join(
                    [
                        self.emojis[self.grid[y][x]]
                        if (
                            (y, x)
                            not in self.players[self.playerOne.id]["l"]
                            + self.players[self.playerTwo.id]["l"]
                        )
                        or end
                        else self.animated_emojis[self.grid[y][x]]
                        for x in range(len(self.grid[y]))
                    ]
                )
                for y in range(len(self.grid))
            ]
        )

