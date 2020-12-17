import random
import math


class _Filler:
    def __init__(self, size, playerOne, playerTwo, server):
        self.game_started = False
        self.size = [size[0] + 2, size[1] + 2]
        # self.sprites = ['R ', 'O ', "Y ", 'G ', 'B ', "P "]
        # self.sprites = [
        #     u"\U0001F494",
        #     u"\U0001F497",
        #     u"\U0001F49B",
        #     u"\U0001F49A",
        #     u"\U0001F499",
        #     u"\U0001F49C",
        #     u"\u2B1B",
        # ]
        self.oneColour = []
        self.twoColour = []
        self.turn = -1
        self.run_level = True
        self.sprites = [
            "<:red:782108442998997003>",
            "<:blue:782108442851803158>",
            "<:green:782108443418689536>",
            "<:yellow:782108443225751552>",
            "<:purple:782108443284733962>",
            "<:black:782108442835812374>",
            "",
        ]
        # self.player_sprites = [
        #     u"\U0001F494",
        #     u"\U0001F497",
        #     u"\U0001F49B",
        #     u"\U0001F49A",
        #     u"\U0001F499",
        #     u"\U0001F49C",
        #     u"\u2B1B",
        # ]
        self.player_sprites = [
            "<a:redg:782108443238465556>",
            "<a:blueg:782108443045134387>",
            "<a:greeng:782108443184070696>",
            "<a:yellowg:782108443179876352>",
            "<a:purpleg:782108443296530432>",
            "<a:blackg:782108443124695092>",
        ]

        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.server = server
        self.message = None
        self.timer = None

        self.fill_board()

        self.current_player = self.playerTwo

    def fill_board(self):
        # creates playing space
        self.grid = [random.randint(0, 5)]

        for i in range(1, self.size[0] * self.size[1]):
            temp = [0, 1, 2, 3, 4, 5]

            try:
                temp.remove(self.grid[i - 1])
                temp.remove(self.grid[i - self.size[0]])
            except Exception:
                pass
            self.grid.append(random.choice(temp))

        # for i in range(self.size[0] * self.size[1]):
        #

        self.oneColour.append(71)
        self.twoColour.append(18)

        self.grid[18] = (
            self.grid[18]
            if self.grid[71] != self.grid[18]
            else (self.grid[18] + 1)
            if self.grid[18] + 1 <= 5
            else self.grid[18] - 1
        )

        self.one_pick = self.grid[71]
        self.two_pick = self.grid[18]

        # sets outer walls
        for y in range(self.size[1]):
            for i in range(self.size[0]):
                if y == 0 or y == self.size[1] - 1:
                    self.grid[i + (self.size[0] * y)] = 6
                else:
                    self.grid[(self.size[0] * y)] = 6
                    self.grid[(self.size[0] * y) + self.size[0] - 1] = 6

        self.update_player()

    def update_player(self):
        if self.run_level:
            if self.turn == 1:
                self.current_player = self.playerTwo
                self.current_colour = self.two_pick
                for pos in self.oneColour:
                    self.grid[pos] = self.one_pick

                    # if (self.grid[pos]) != (self.grid[pos - self.size[0]]) or (self.grid[pos]) != (self.grid[pos + 1])
                    if (self.grid[pos]) == (self.grid[pos - self.size[0]]):
                        if abs(pos - self.size[0]) not in self.oneColour:
                            self.oneColour.append(abs(pos - self.size[0]))

                    if (self.grid[pos]) == (self.grid[pos + 1]):
                        if (pos + 1) not in self.oneColour:
                            self.oneColour.append(pos + 1)

                    if (self.grid[pos]) == (self.grid[pos + self.size[0]]):
                        if (pos + self.size[0]) not in self.oneColour:
                            self.oneColour.append((pos + self.size[0]))

                    if (self.grid[pos]) == (self.grid[pos - 1]):
                        if abs(pos - 1) not in self.oneColour:
                            self.oneColour.append(abs(pos - 1))

            elif self.turn == -1:
                self.current_player = self.playerOne
                for pos in self.twoColour:
                    self.grid[pos] = self.two_pick
                    self.current_colour = self.one_pick

                    if (self.grid[pos]) == (self.grid[pos - self.size[0]]):
                        if abs(pos - self.size[0]) not in self.twoColour:
                            self.twoColour.append(abs(pos - self.size[0]))

                    if (self.grid[pos]) == (self.grid[pos + 1]):
                        if (pos + 1) not in self.twoColour:
                            self.twoColour.append(pos + 1)

                    if (self.grid[pos]) == (self.grid[pos + self.size[0]]):
                        if (pos + self.size[0]) not in self.twoColour:
                            self.twoColour.append((pos + self.size[0]))

                    if (self.grid[pos]) == (self.grid[pos - 1]):
                        if abs(pos - 1) not in self.twoColour:
                            self.twoColour.append(abs(pos - 1))

        self.amountOne = len(self.oneColour)
        self.amountTwo = len(self.twoColour)

        self.turn *= -1
        if self.amountOne + self.amountTwo == ((self.size[0] - 2) * (self.size[1] - 2)):
            self.run_level = False

    def get_winner(self):
        winner = (
            self.playerOne
            if self.amountOne > self.amountTwo
            else self.playerTwo
            if self.amountOne != self.amountTwo
            else False
        )
        return winner

    def draw_board(self):
        # sets self.sprites
        self.tempGrid = list(self.grid)
        for i in range(len(self.tempGrid)):
            self.tempGrid[i] = self.sprites[self.grid[i]]
        if self.run_level:
            tempColors = self.oneColour + self.twoColour
            for p in tempColors:
                self.tempGrid[p] = self.player_sprites[
                    self.sprites.index(self.tempGrid[p])
                ]

        # creates printable string
        self.game_grid = ""
        for y in range(self.size[1]):
            row = ""
            for x in range(self.size[0]):
                row += str(self.tempGrid[x + (self.size[0] * y)])
            row += "\n"
            self.game_grid += row

    def __str__(self):
        self.draw_board()
        return self.game_grid
