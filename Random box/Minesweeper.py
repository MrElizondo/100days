#Minesweeper

import numpy as np
from random import randrange


class Board:
    def __init__ (self, height, width, mines):
        '''Initializes a game creating a board with mines and filled-in numbers.'''
        self.board = np.zeros((height,width))
        
        #Populate board with mines
        while mines != 0:
            x = randrange(height)
            y = randrange(width)
            if self.board[x,y] == 0:
                self.board[x,y] = 9
                mines -= 1
        
        #Fill up numbers in board
        for x in range(height):
            for y in range(width):
                if self.board[x,y] != 9:
                    count = 0
                    for i in range(-1,2):
                        for j in range(-1,2):
                            skip = (x+i == -1) or (x+i == height) or (y+j == -1) or (y+j == width)
                            if not skip and self.board[x+i,y+j] == 9:
                                count += 1
                    self.board[x,y] = count


game = Board(10,12,20)
print(game.board)