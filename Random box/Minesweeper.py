#Minesweeper

import numpy as np
from random import randrange
from os import system


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
        
        return '\n'.join([''.join([chr(int(c)) for c in row]) for row in output])

    
    def shape (self):
        width, height, _ = np.shape(self.board)
        return width, height
    
    
    def print(self):
        system('cls')
        print(self)
    
    
    def request_dimensions ():
        '''Requests board dimensions and mine number and validates them.'''
        valid = False
        while not valid:
            width =  input('Enter number of columns: ')
            try:
                width = int(width)
                assert width > 0
                valid = True
            except: print('Please enter a positive number.')

        valid = False
        while not valid:
            height = input('Enter number of rows: ')
            try:
                height = int(height)
                assert height > 0
                valid = True
            except: print('Please enter a positive number.')

        valid = False
        while not valid:
            mines =  input('Enter number of mines: ')
            try:
                mines = int(mines)
                assert mines > 0
                if mines >= height*width: print('There are too many mines.')
                else:                     valid = True
            except: print('Please enter a positive number.')
        
        return width, height, mines
    
    
    def reveal (self, column, row):
        '''Given a location on the board, this method reveals the number in that tile by changing
        its visibility value to 1. If the number is 0, it also triggers reveal for all neighbouring
        tiles. If the tile contains a mine, the function will return True, if not False.'''
        number = self.board[column, row, 0]
        self.board[column, row, 1] = 1
        
        if number == 9:
            return True
        elif number == 0:
            for i in range(-1,2):
                for j in range(-1,2):
                    if (not (i == 0 and j == 0)) and (column + i >= 0) and (row + j >= 0):
                        visibility = self.board[column+i, row+j, 1]
                        if not visibility:
                            try: self.reveal(column + i, row + j)
                            except: pass
        return False
    
    
    def final_reveal (self, winner_winner_chicken_dinner):
        '''Reveals the whole board for when a player wins.'''
        width, height, _ = np.shape(self.board)
        for i in range(width):
            for j in range(height):
                if winner_winner_chicken_dinner:
                    self.board[i,j,1] = 1
                else:
                    if self.board[i,j,0] == 9: self.board[i,j,1] = 1
    
    
    def request_coordinates (self):
        '''Requests coordinates of a tile and validates them.'''
        width, height, _ = np.shape(self.board)
        
        valid = False
        while not valid:
            valid_x, valid_y = False, False
            
            while not valid_x:
                x = input('Enter a column number (columns start with 1): ')
                try:
                    x = int(x)
                    assert x > 0
                    assert x <= width
                    valid_x = True
                except:
                    print('The number must be positive and less or equal to ' + str(width) + '.')
            x -= 1
            
            while not valid_y:
                y = input('Enter a column number (rows start with 1): ')
                try:
                    y = int(y)
                    assert y > 0
                    assert y <= height
                    valid_y = True
                except:
                    print('The number must be positive and less or equal to ' + str(height) + '.')
            y -= 1
            
            if self.board[x,y,1] == 1:
                print('That tile is already visible, please choose a different one.')
            else:
                valid = True
        
        return x, y
            

    def is_won (self):
        '''Returns True only if all non-mine tiles are visible.'''
        width, height, _ = np.shape(self.board)

        for i in range(width):
            for j in range(height):
                if self.board[i,j,0] != 9 and self.board[i,j,1] == 0:
                    return False
        return True
    
    
    def is_lost (self):
        '''Returns True if any of the mines are visible.'''
        width, height, _ = np.shape(self.board)

        for i in range(width):
            for j in range(height):
                if self.board[i,j,0] == 9 and self.board[i,j,1] == 1:
                    return True
        return False


    def new_game (self, winner_winner_chicken_dinner):
        '''Asks if the user wants to have another game after game is over.
        Returns True or False.'''
        if winner_winner_chicken_dinner: message = 'Congratulations, you won!'
        else:                            message = 'Oh no, you lost!'

        answer = ''
        while answer.upper() not in ('Y', 'YES', 'N', 'NO'):
            print('\n' + message + '\n')
            answer = input('Fancy another game? ')
        
        return answer.upper() in ('Y', 'YES')


#MAIN LOOP
while True:
    system('cls')
    width, height, mines = Board.request_dimensions()
    game = Board(width, height, mines)
    game.print()

    first = True
    while True:
        x, y = game.request_coordinates()
        if first: #In the first iteration, if the tile contains a mine the board reshuffles.
            while game.board[x,y,0] == 9:
                game = Board(width, height, mines)
            first = False
        game.reveal (x,y)
        game.print()
        
        winner = game.is_won()
        loser  = game.is_lost()
        if loser:
            game.final_reveal (False)
            game.print()
            again = game.new_game(False)
        elif winner:
            game.final_reveal (True)
            game.print()
            again = game.new_game(True)
        
        if winner or loser:
            if again:
                break
            else:
                print('\n' + 'OK, have a nice day!')
                system('pause')
                quit()        