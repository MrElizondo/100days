#Minesweeper

import numpy as np
from random import randrange


class Board:
    def __init__ (self, width, height, mines):
        '''Initializes a game creating a board with mines and filled-in numbers.'''
        self.board = np.zeros((width,height,2))
        
        #Populate board with mines
        while mines != 0:
            x = randrange(width)
            y = randrange(height)
            if self.board[x,y,0] == 0:
                self.board[x,y,0] = 9
                mines -= 1
        
        #Fill up numbers in board
        for x in range(width):
            for y in range(height):
                if self.board[x,y,0] != 9:
                    count = 0
                    for i in range(-1,2):
                        for j in range(-1,2):
                            skip = (x+i == -1) or (x+i == width) or (y+j == -1) or (y+j == height)
                            if not skip and self.board[x+i,y+j,0] == 9:
                                count += 1
                    self.board[x,y,0] = count
                    
                    
    def __str__ (self):
        '''Outputs the board ready to be printed.'''
        output = []
        width, height, _ = np.shape(self.board)
        
        first_row = [9556,9552,9552,9552]
        for i in range(width-1): first_row = first_row + [9572,9552,9552,9552]
        first_row.append(9559)
        output.append(first_row)
        
        sep_row = [9567]
        for j in range(width-1):
            sep_row = sep_row + [9472,9472,9472,9532]
        sep_row = sep_row + [9472,9472,9472,9570]
        
        last_row = [9562,9552,9552,9552]
        for i in range(width-1): last_row = last_row + [9575,9552,9552,9552]
        last_row.append(9565)
        
        for i in range(height):
            num_row = []
            
            num_row.append(9553)
            num_row.append(32)
            for j in range(width):
                number, visible = self.board[j,i,0], self.board[j,i,1]
                if visible:
                    if number == 0:
                        num_row.append(32)
                    elif number <= 8:
                        num_row.append(number+48) #+48 so it's then converted to the number in unicode
                    else:
                        num_row.append(164)
                else:
                    num_row.append(63)
                num_row.append(32)
                num_row.append(9474)
                num_row.append(32)
            num_row.pop(-1)
            num_row.pop(-1)
            num_row.append(9553)
            
            output.append(num_row)
            output.append(sep_row)
        
        output.pop(-1)
        output.append(last_row)
        
        return '\n'.join([''.join([chr(c) for c in row]) for row in output])



game = Board(3,4,3)
print(game)