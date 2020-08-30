import random
import math

import random
import math


class Filler:
    def __init__(self, size, playerOne, playerTwo, server, msg):
        self.size = [size[0] + 2, size[1] + 2]
        # self.sprites = ['R ', 'O ', "Y ", 'G ', 'B ', "P "]
        # self.sprites = [u"\U0001F494", 	u"\U0001F497", 	u"\U0001F49B", 	u"\U0001F49A", 	u"\U0001F499", 	u"\U0001F49C", u"\u2B1B"]
        self.oneColour = []
        self.twoColour = []
        self.turn = -1
        self.run_level = True
        self.sprites = [
            ":red_square:",
            ":orange_square:",
            ":yellow_square:",
            ":green_square:",
            ":blue_square:",
            ":purple_square:",
            ":black_large_square:",
        ]

        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.server = server
        self.message = msg
        self.timer = None

        self.fill_board()

        self.current_player = self.playerTwo

    def fill_board(self):
        # creates playing space
        self.grid = []
        for i in range(self.size[0] * self.size[1]):
            self.grid.append(random.randint(0, 5))

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

        # creates printable string
        self.game_grid = ""
        for y in range(self.size[1]):
            row = ""
            for x in range(self.size[0]):
                row += str(self.tempGrid[x + (self.size[0] * y)])
            row += "\n"
            self.game_grid += row

