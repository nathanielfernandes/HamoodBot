import chess


class _Chess:
    def __init__(self, playerOne, playerTwo, server):
        self.game_started = False
        self.turn = -1
        self.run_game = True
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
        self.sprites = {
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
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.server = server
        self.message = None
        self.timer = None
        self.winner = None
        self.reason = None
        self.board = chess.Board()
        self.move = ""
        self.current_player = {1: self.playerOne, -1: self.playerTwo}

    def update_game(self):
        if self.run_game:
            try:
                square = chess.parse_square(self.move[:2])
                # print(square)
                color = self.board.color_at(square=square)
            except ValueError:
                return "Invalid Move"

            if (self.turn == -1 and color) or (self.turn == 1 and not color):
                try:
                    self.board.push_san(self.move)
                except ValueError:
                    return "Invalid Move"
                self.turn *= -1
            else:
                return "Not Your Piece"

    def check_end(self):
        if self.board.is_game_over():
            result = self.board.result()
            self.run_game = False

            if result == "1-0":
                self.winner = -1
            elif result == "0-1":
                self.winner = 1
            else:
                self.winner = "DRAW"

            if self.board.is_checkmate():
                self.reason = "Checkmate"
            elif self.board.is_stalemate():
                self.reason = "Stalemate"

    def draw_board(self):
        p = "".join(str(self.board).split())

        tempBoard = []
        c = 1
        flip = 1
        for i in range(len(p)):
            tempBoard.append(self.sprites[f"{p[i]}{'W' if flip > 0 else 'B'}"])
            flip *= -1
            if c == 8:
                flip *= -1
                c = 0
            c += 1

        if self.turn > 0:
            tempBoard = tempBoard[::-1]
        self.legendX = self.legendX[::-1]
        self.legendY = self.legendY[::-1]

        n = 0
        for i in range(0, len(tempBoard), 8):
            tempBoard[i] = f"{self.legendX[n]}{tempBoard[i]}"
            n += 1

        self.game_board = []
        for i in range(0, len(tempBoard), 8):
            self.game_board.append("".join(tempBoard[i : i + 8]))

        self.game_board = (
            "\n".join(self.game_board)
            + "\n<:hamood:713523447141236867>"
            + "".join(self.legendY)
        )

