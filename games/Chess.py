import chess
import discord
from games.DefaultGame import DefaultGame


class Chess(DefaultGame):
    def __init__(
        self, ctx, bot, playerTwo=None, wager: int = 0,
    ):
        super().__init__(
            ctx=ctx,
            bot=bot,
            playerTwo=playerTwo,
            wager=wager,
            game_name="chess",
            thumbnail="https://cdn.discordapp.com/attachments/749779300181606411/776368591557754910/unknown.png",
        )
        self.legendX = [
            ":one:",
            ":two:",
            ":three:",
            ":four:",
            ":five:",
            ":six:",
            ":seven:",
            ":eight:",
        ]
        self.legendY = [
            "<:chessA:776347125272412161>",
            "<:chessB:776347122341249044>",
            "<:chessC:776347121694539777>",
            "<:chessD:776347122496831498>",
            "<:chessE:776347122336792606>",
            "<:chessF:776347122161025054>",
            "<:chessG:776347121796251660>",
            "<:chessH:776347122282266644>",
        ][::-1]
        self.emojis = {
            "rW": "<:rW:776325516009144341>",
            "rB": "<:rB:776325516063539221>",
            "nW": "<:nW:776325516473925632>",
            "nB": "<:nB:776325515946491915>",
            "bW": "<:bW:776325516047286322>",
            "bB": "<:bB:776325516071272458>",
            "qW": "<:qW:776325515249975316>",
            "qB": "<:qB:776325515563761704>",
            "kW": "<:kW:776325515287199775>",
            "kB": "<:kB:776325515211964457>",
            "pW": "<:pW:776325516222267415>",
            "pB": "<:pB:776325516042698763>",
            "RW": "<:RW:776325515786453012>",
            "RB": "<:RB:776325515870863361>",
            "NW": "<:NW:776325515665080351>",
            "NB": "<:NB:776325515912937522>",
            "BW": "<:BW:776325515631788052>",
            "BB": "<:BB:776325515564679189>",
            "QW": "<:QW:776325515665211452>",
            "QB": "<:QB:776325515312365568>",
            "KW": "<:KW:776325515195187202>",
            "KB": "<:KB:776325515589451776>",
            "PW": "<:PW:776325515866669077>",
            "PB": "<:PB:776325516076253205>",
            ".W": "<:W_:776325516118065152>",
            ".B": "<:B_:776325516096569384>",
            " W": "",
            " B": "",
            "\nW": "\n",
            "\nB": "\n",
        }

        self.players = {
            self.playerOne.id: {
                "c": discord.Color.from_rgb(245, 245, 220),
                "e": "<:W_:776325516118065152>",
            },
            self.playerTwo.id: {
                "c": discord.Color.blue(),
                "e": "<:B_:776325516096569384>",
            },
        }

    async def game_start(self):
        self.board = chess.Board()
        content, embed = self.create_content_embed()
        await self.update_message(embed=embed, content=content)

    async def game_update(self, member, move):
        if member == self.current_turn:
            try:
                square = chess.parse_square(move[:2])
                color = self.board.color_at(square=square)
            except ValueError:
                return "Invalid Move"

            if (member == self.playerTwo and color) or (
                member == self.playerOne and not color
            ):
                try:
                    self.board.push_san(move)
                except ValueError:
                    return "Invalid Move"

                self.swap_turns()
                p, r = self.check_end()

                winner, loser, tie = None, None, False
                if p != 0:
                    if p == 1:
                        tie = True
                    else:
                        winner, loser = p[0]

                    await self.end_game(winner=winner, loser=loser, tie=tie)

                content, embed = self.create_content_embed(
                    winner=winner, tie=tie, result=r
                )
                await self.update_message(content=content, embed=embed)
                return
            else:
                return "Not Your Piece"
        else:
            return "It's Not Your Turn"

    def create_content_embed(self, winner=None, tie=False, result=""):
        if tie:
            color = discord.Color.from_rgb(0, 0, 0)
            title = "It's a draw!"
        elif winner is not None:
            color = self.players[winner.id]["c"]
            title = f"{self.players[winner.id]['e']} **{winner}** won by {result}!"
        else:
            color = self.players[self.current_turn.id]["c"]
            title = (
                f"{self.players[self.current_turn.id]['e']} {self.current_turn}'s Turn"
            )

        value = f"wager: {self.cash(self.wager)}" if self.wager > 0 else ""
        embed = discord.Embed(
            title=title,
            description=f"**{self.playerOne}** vs. **{self.playerTwo}**\nuse `{self.prefix}move` to play\n{value}",
            color=color,
        )
        content = self.draw_board()
        # embed.set_author(name=self.game_name.title(), icon_url=self.thumbnail)

        return content, embed

    def check_end(self):
        if self.board.is_game_over():
            result = self.board.result()
            if result == "1-0":
                winner = (self.playerTwo, self.playerOne)
            elif result == "0-1":
                winner = (self.playerOne, self.playerTwo)
            else:
                winner = 1, "Tie"

            reason = "NA"
            if self.board.is_checkmate():
                reason = "Checkmate"
            elif self.board.is_stalemate():
                reason = "Stalemate"

            return winner, reason

        return 0, ""

    def draw_board(self):
        p = "".join(str(self.board).split())

        tempBoard = []
        c = 1
        flip = 1
        for i in range(len(p)):
            tempBoard.append(self.emojis[f"{p[i]}{'W' if flip > 0 else 'B'}"])
            flip *= -1
            if c == 8:
                flip *= -1
                c = 0
            c += 1

        if self.current_turn == self.playerOne:
            tempBoard = tempBoard[::-1]
        self.legendX = self.legendX[::-1]
        self.legendY = self.legendY[::-1]

        n = 0
        for i in range(0, len(tempBoard), 8):
            tempBoard[i] = f"{self.legendX[n]}{tempBoard[i]}"
            n += 1

        final = []
        for i in range(0, len(tempBoard), 8):
            final.append("".join(tempBoard[i : i + 8]))

        return (
            "\n".join(final) + "\n<:hamood:713523447141236867>" + "".join(self.legendY)
        )

