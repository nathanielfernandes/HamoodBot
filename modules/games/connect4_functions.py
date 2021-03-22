class Connect_Four:
    def __init__(self, size, playerOne, playerTwo, server):
        self.game_started = False
        self.size = [size[0] + 2, size[1] + 1]
        self.turn = -1
        self.run_level = True
        # self.sprites = ["  ", "# ", "o ", "x "]
        self.sprites = [
            "<:empty:823351307279663145>",
            "<:border:823347606074687539>",
            "<:redinside:823347539813335071>",
            "<:yellowinside:823347539724992522>",
            # "<:redcircle:823347539460882453>",
            # "<:yellowcircle:823347539495092226>",
            "<:leftside:823351703402578001>",
            "<:rightside:823351703842979880>",
            "<:one:823355865481871390>",
            "<:two:823355865380945951>",
            "<:three:823355865376751638>",
            "<:four:823355865348177930>",
            "<:five:823355865138331649>",
            "<:six:823355865247383594>",
            "<:seven:823355865431801856>",
            "<:redcircle:823347539460882453>",
            "<:yellowcircle:823347539495092226>",
        ]
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.onePeices = []
        self.twoPeices = []
        self.server = server
        self.message = None
        self.timer = None
        self.choice = None
        self.winner = None

        self.fill_board()
        self.current_player = self.playerTwo

    def fill_board(self):
        self.grid = [0 for i in range(self.size[0] * self.size[1])]
        n = -1
        # sets outer walls
        for y in range(self.size[1]):
            for i in range(self.size[0]):
                if y == self.size[1] - 1:
                    if n == -1:
                        self.grid[i + (self.size[0] * y)] = 4
                    elif n == 7:
                        self.grid[i + (self.size[0] * y)] = 5
                    else:
                        self.grid[i + (self.size[0] * y)] = 6 + n
                    n += 1
                # else:
                self.grid[(self.size[0] * y)] = 4
                self.grid[(self.size[0] * y) + self.size[0] - 1] = 5

    def update_player(self):
        def place_peice(self, peice):
            for i in range(0, len(self.grid), self.size[0]):
                if (
                    self.grid[i + self.choice] == 0
                    and self.grid[i + self.choice + self.size[0]] > 0
                ):
                    self.grid[self.choice + i] = peice
                    self.turn *= -1

                    return self.choice + i

        if self.run_level:
            if self.choice is not None:
                if self.turn == 1:
                    placed = place_peice(self, 2)
                    if placed is not None:
                        self.onePeices.append(placed)
                        self.current_player = self.playerTwo

                elif self.turn == -1:
                    placed = place_peice(self, 3)
                    if placed is not None:
                        self.twoPeices.append(placed)
                        self.current_player = self.playerOne

    def check_win(self):
        if len(self.onePeices) + len(self.twoPeices) == (self.size[0] - 2) * (
            self.size[1] - 1
        ):
            self.run_level = False
            self.winner = "Tie"
            i = 2

        else:
            for i in range(len(self.grid)):
                connected, connected1, connected2, connected3 = 1, 1, 1, 1
                if self.grid[i] == 2 or self.grid[i] == 3:
                    for j in range(1, 4):
                        if self.grid[i + j] == self.grid[i]:
                            connected += 1
                        # elif self.grid[i + j] == 1:
                        else:
                            connected = 1
                            break

                    for j in range(1, 4):
                        if self.grid[i + j * self.size[0]] == self.grid[i]:
                            connected1 += 1
                        else:
                            # elif self.grid[i + j * self.size[0]] == 1 or self.grid[i + j * self.size[0]] != :
                            connected1 = 1
                            break

                    for j in range(1, 4):
                        if self.grid[i + j * self.size[0] + j] == self.grid[i]:
                            connected2 += 1
                        # elif self.grid[i + j * self.size[0] + j] == 1:
                        else:
                            connected2 = 1
                            break

                    for j in range(1, 4):
                        if self.grid[i + j * self.size[0] - j] == self.grid[i]:
                            connected3 += 1
                        # elif self.grid[i + j * self.size[0] - j] == 1:
                        else:
                            connected3 = 1
                            break

                if (
                    connected == 4
                    or connected1 == 4
                    or connected2 == 4
                    or connected3 == 4
                ):
                    if self.grid[i] == 2:
                        self.winner = self.playerOne
                    elif self.grid[i] == 3:
                        self.winner = self.playerTwo
                    self.run_level = False
                    break
        return self.winner, self.grid[i]

    def draw_board(self):
        # sets self.sprites
        self.tempGrid = [
            self.sprites[self.grid[i]] for i in range(len(list(self.grid)))
        ]
        # creates printable string
        self.game_grid = "\n".join(
            [
                "".join(
                    [
                        str(self.tempGrid[x + (self.size[0] * y)])
                        for x in range(self.size[0])
                    ]
                )
                for y in range(self.size[1])
            ]
        )
        # print(self.game_grid)


# game = Connect_Four([7, 6], "player 1", "player 2", "123")
# game.draw_board()
# print(game.game_grid)
# while game.run_level:
#     game.draw_board()

#     #     # print(
#     #     #     len(game.onePeices),
#     #     #     len(game.twoPeices),
#     #     #     (game.size[0] - 2) * (game.size[1] - 1),
#     #     # )
#     game.choice = int(input(f"{game.current_player} enter: "))
#     print()
#     game.update_player()
