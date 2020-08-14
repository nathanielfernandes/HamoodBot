# Sokoban in the Terminal
import random

class Soko_ban():
    def __init__(self, size, user, msg):
        self.size = [size[0]+2, size[1]+2]
        self.grid = []
        #self.sprites = ['  ', '# ', '☒ ','o ', 'x ', '@ ']
        self.sprites = [':black_large_square:', ':white_large_square:', ':blue_square:', ':white_large_square:', ':x:', ':pensive:', ':kissing_heart:']
        self.level = 1
        self.run_level = True
        self.completed = 0
        
        self.move = None
        self.moves = 0
        #discord
        self.theme_num = random.randint(0,7)
        self.user = user
        self.message = msg
        self.timer = None

        self.game_start()

    def game_start(self):
        self.start_game = True

        if self.start_game:
            if not self.run_level:
   
                self.run_level = True
                self.level += 1

                if self.level <= 25:
                    if (self.level%5) == 0:
                        self.size[0] += 1
                        self.size[1] += 1

            self.run_level = True
            self.create_level()


    def create_level(self):
        check = int(self.level) if self.level <= 34 else 34
        #creates playing space
        self.grid = []

        for i in range(self.size[0]*self.size[1]):
            self.grid.append(0)

        #sets outer walls
        for y in range(self.size[1]):
            for i in range(self.size[0]):
                if y == 0 or y == self.size[1]-1:
                    self.grid[i+(self.size[0]*y)] = 1
                else:
                    self.grid[(self.size[0]*y)] = 1
                    self.grid[(self.size[0]*y) + self.size[0]-1] = 1


        #finds available spots for boxes
        self.box_grid = list(self.grid)
        for y in range(self.size[1]):
            for i in range(1, self.size[0]-1):
                if y == 1 or y == self.size[1]-2:
                    self.box_grid[i+(self.size[0]*y)] = 1
                else:
                    self.box_grid[(self.size[0]*y+1)] = 1
                    self.box_grid[(self.size[0]*y+1) + self.size[0]-3] = 1

        #plots spots
        self.spots = []
        for i in range(len(self.box_grid)):
            if self.box_grid[i] == 0:
                self.spots.append(i)

        self.box_pos = []
        #adds boxes
        for i in range(check-(check//2)):
            placement = random.choice(self.spots)
            self.grid[placement] = 2
            (self.spots).remove(placement)
            self.box_pos.append(placement)

        #finds empty spots
        self.spots = [] 
        for i in range(len(self.grid)):
            if self.grid[i] == 0:
                self.spots.append(i)

        #adds player
        placement = random.choice(self.spots)
        self.grid[placement] = 5
        (self.spots).remove(placement)
        self.player_pos = placement

        self.goal_pos = []
        #adds goals
        for i in range(check-(check//2)):
            placement = random.choice(self.spots)
            self.grid[placement] = 4
            (self.spots).remove(placement)
            self.goal_pos.append(placement)


        #temporary backup of current level
        self.reserve_grid = list(self.grid)
        self.reserve_player = int(self.player_pos)
        self.reserve_box = list(self.box_pos)

                #checks if level may be impossible
        for pos in self.box_pos:
            if (pos in self.box_pos) and (pos+1 in self.box_pos) and (pos+self.size[0] in self.box_pos) and (pos+self.size[0]+1 in self.box_pos):
                self.create_level()

        return self.grid
    

    def player_move(self):
        if self.run_level:
            self.draw_board()

            self.new_player_pos = int(self.player_pos)

            #finds new location of player after movement
            self.last_move = ''
            if self.move == 'up': 
                self.new_player_pos -= int(self.size[0])
                self.moves += 1
            elif self.move == 'down': 
                self.new_player_pos += int(self.size[0])
                self.moves += 1
            elif self.move == 'left': 
                self.new_player_pos -= 1
                self.moves += 1
            elif self.move == 'right': 
                self.new_player_pos += 1
                self.moves += 1

            #resets level
            elif self.move == 'reset':
                self.grid = list(self.reserve_grid)
                self.player_pos = int(self.reserve_player)
                self.box_pos = list(self.reserve_box)
                self.new_player_pos = int(self.player_pos)

            elif self.move == 'shuffle':
                self.create_level()
                self.grid = list(self.reserve_grid)
                self.player_pos = int(self.reserve_player)
                self.box_pos = list(self.reserve_box)
                self.new_player_pos = int(self.player_pos)

            #ends game
            elif self.move == 'end':
                self.run_level = False
                self.start_game = False
            
            elif self.move == 'next':
                self.box_pos = list(self.goal_pos)

            self.update_board()
            

    def update_board(self):
        #checks if player is blocked by wall
        if self.grid[self.new_player_pos] != 1:
            
            #checks if player is trying to push a block
            if self.grid[self.new_player_pos] in [2,3]:
                
                #handles player interactions with boxes
                if self.move == 'up':
                    if self.grid[self.new_player_pos - self.size[0]] not in [1,2,3]:
                        self.grid[self.new_player_pos] = 5
                        self.box_pos[(self.box_pos).index(self.new_player_pos)] = self.new_player_pos - self.size[0]
                    else:
                        return

                elif self.move == 'down':
                    if self.grid[self.new_player_pos + self.size[0]] not in [1,2,3]:
                        self.grid[self.new_player_pos] = 5
                        self.box_pos[(self.box_pos).index(self.new_player_pos)] = self.new_player_pos + self.size[0]
                    else:
                        return

                elif self.move == 'left':
                    if self.grid[self.new_player_pos - 1] not in [1,2,3]:
                        self.grid[self.new_player_pos] = 5
                        self.box_pos[(self.box_pos).index(self.new_player_pos)] = self.new_player_pos - 1
                    else:
                        return

                elif self.move == 'right':
                    if self.grid[self.new_player_pos + 1] not in [1,2,3]:
                        self.grid[self.new_player_pos] = 5
                        self.box_pos[(self.box_pos).index(self.new_player_pos)] = self.new_player_pos + 1
                    else:
                        return

            #moves player
            self.grid[self.player_pos] = 0
            self.grid[self.new_player_pos] = 5
            self.player_pos = int(self.new_player_pos)
            
            #replaces goals
            for pos in self.goal_pos:
                if self.player_pos != pos:
                    self.grid[pos] = 4
            #replaces boxes
            for pos in self.box_pos:
                self.grid[pos] = 2
            
            self.completed = 0
            for box in self.box_pos:
                if box in self.goal_pos:
                    self.grid[box] = 3
                    self.completed += 1

            #checks if all boxes are over thier goals
            if sorted(self.box_pos) == sorted(self.goal_pos):
                self.run_level = False
                self.grid[self.player_pos] = 6
                self.draw_board()


    def draw_board(self):
        #sets self.sprites
        self.tempGrid = list(self.grid)
        for i in range(len(self.tempGrid)):
            self.tempGrid[i] = self.sprites[self.grid[i]]

        #creates printable string
        self.game_grid = ''
        for y in range(self.size[1]):
            row = ''
            for x in range(self.size[0]):
                row += str(self.tempGrid[x+(self.size[0]*y)])
            row += '\n'
            self.game_grid += row
  
        