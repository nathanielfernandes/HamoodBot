import random


class TwentyFortyEight:
    def __init__(self, user, server):
        self.grid = []
        self.sprites = [
            "<:empty:775638765410320394>",
            ":black_large_square:",
            "<:2_:775636041565732874>",
            "<:4_:775636041473458176>",
            "<:8_:775636041624977408>",
            "<:16:775636041700474880>",
            "<:32:775636041201614869>",
            "<:64:775636041234120715>",
            "<:128:775636041586704404>",
            "<:256:775636041327312907>",
            "<:512:775636041541222400>",
            "<:1024:775636041666265108>",
            "<:2048:775636041540435999>",
            "4096 ",
            "8192 ",
            "16384 ",
        ]

        self.run_game = True
        self.user = user
        self.server = server
        self.message = None
        self.timer = None
        self.move = None
        self.moves = 0
        self.score = 0
        self.fill_board()
        self.spawn_random()
        self.spawn_random()

        self.updates = {
            "up": self.move_up,
            "down": self.move_down,
            "left": self.move_left,
            "right": self.move_right,
        }

    def fill_board(self):
        self.grid = [[0] * 4 for i in range(4)]

    def spawn_random(self):
        r = random.randint(0, 3)
        c = random.randint(0, 3)

        while self.grid[r][c] != 0:
            r = random.randint(0, 3)
            c = random.randint(0, 3)

        self.grid[r][c] = 2

    def game_end(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True

        for i in range(3):
            for j in range(3):
                if (
                    self.grid[i][j] == self.grid[i + 1][j]
                    or self.grid[i][j] == self.grid[i][j + 1]
                ):
                    return True

        for j in range(3):
            if self.grid[3][j] == self.grid[3][j + 1]:
                return True

        for i in range(3):
            if self.grid[i][3] == self.grid[i + 1][3]:
                return True

        self.run_game = False
        return False

    def compress_grid(self, grid):
        # empty grid
        new_grid = [[0] * 4 for i in range(4)]

        for i in range(4):
            k = 0
            for j in range(4):
                if grid[i][j] != 0:
                    new_grid[i][k] = grid[i][j]
                    k += 1

        return new_grid

    def merge_grid(self, grid):
        for i in range(4):
            for j in range(3):
                if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                    grid[i][j] = grid[i][j] + 1
                    self.score += 2 ** (grid[i][j] - 1)
                    grid[i][j + 1] = 0

        return grid

    def reverse_grid(self, grid):
        new_grid = []
        for i in range(4):
            new_grid.append([])
            for j in range(4):
                new_grid[i].append(grid[i][3 - j])

        return new_grid

    def transpose_grid(self, grid):
        new_grid = []
        for i in range(4):
            new_grid.append([])
            for j in range(4):
                new_grid[i].append(grid[j][i])

        return new_grid

    def move_left(self, grid):
        return self.compress_grid(self.merge_grid(self.compress_grid(grid)))

    def move_right(self, grid):
        return self.reverse_grid(self.move_left(self.reverse_grid(grid)))

    def move_up(self, grid):
        return self.transpose_grid(self.move_left(self.transpose_grid(grid)))

    def move_down(self, grid):
        return self.transpose_grid(self.move_right(self.transpose_grid(grid)))

    def update_game(self):
        if self.move in self.updates:
            self.grid = self.updates[self.move](self.grid)

    def draw_board(self):

        temp = list(self.grid)
        self.game_grid = "\n".join(
            ["".join([self.sprites[temp[i][j]] for j in range(4)]) for i in range(4)]
        )




# game = TwentyFortyEight("p1", "oli")


# while game.run_game:
#
#     game.move = input(f"{game.user} enter: ")
#     temp = game.grid
#     game.update_game()
#     if game.game_end():
#         if game.grid != temp:
#             game.moves += 1
#             game.spawn_random()
#     else:
#         print(game.moves)


# game.draw_board()
