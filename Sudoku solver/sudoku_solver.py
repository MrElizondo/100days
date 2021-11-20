'''This program attempts to solve sudokus by applying a sequence of common
human techniques.'''

'''
TO DO:
-Method to search rows and columns for values for which all positions fall
    into the same quadrant -> delete from other positions in quadrant.
-Finish re-writing methods in OOP
-Create a way to input the sudoku
-Create a visual interface
'''

import os
from copy import deepcopy
from itertools import combinations
import numpy as np



o = None

test_easy = [[7,9,6,1,4,3,o,5,o],
             [4,5,o,o,o,o,1,3,o],
             [o,1,o,7,o,2,o,o,9],
             [9,3,1,o,o,o,o,o,5],
             [o,o,o,o,o,o,o,o,o],
             [5,o,o,o,o,o,4,9,1],
             [6,o,o,8,o,7,o,2,o],
             [o,7,8,o,o,o,o,1,4],
             [o,2,o,4,3,9,7,6,8]]

test = [[1,7,o,o,9,o,3,o,8],
        [o,o,o,o,1,o,o,o,o],
        [o,5,4,2,o,o,o,o,6],
        [o,o,o,4,o,o,6,o,o],
        [5,o,o,o,7,o,o,o,2],
        [o,o,7,o,o,2,o,o,o],
        [8,o,o,o,o,6,7,3,o],
        [o,o,o,o,4,o,o,o,o],
        [4,o,6,o,5,o,o,8,1]]

test_solved = [[1,7,2,6,9,4,3,5,8],
               [6,8,9,5,1,3,4,2,7],
               [3,5,4,2,8,7,1,9,6],
               [2,1,8,4,3,5,6,7,9],
               [5,6,3,9,7,1,8,4,2],
               [9,4,7,8,6,2,5,1,3],
               [8,9,5,1,2,6,7,3,4],
               [7,2,1,3,4,8,9,6,5],
               [4,3,6,7,5,9,2,8,1]]


class Sudoku:
    class Inconsistent(Exception):
        '''Custom error type to express that the Sudoku is inconsistent.'''
        def __init__(self, message):
            self.message = message
    
    view = True
    view_poss = False
    view_all = True
    
    boxes_small = [
            [9556,9552,9552,9552,9572,9552,9552,9552,9572,9552,9552,9552,9574,9552,9552,9552,9572,9552,9552,9552,9572,9552,9552,9552,9574,9552,9552,9552,9572,9552,9552,9552,9572,9552,9552,9552,9559],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9568,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9571],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9568,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9571],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9474, 32 , 32 , 32 ,9553],
            [9562,9552,9552,9552,9575,9552,9552,9552,9575,9552,9552,9552,9577,9552,9552,9552,9575,9552,9552,9552,9575,9552,9552,9552,9577,9552,9552,9552,9575,9552,9552,9552,9575,9552,9552,9552,9565],
            ]
            
    boxes_big = [
            [9556,9552,9552,9552,9552,9552,9552,9552,9572,9552,9552,9552,9552,9552,9552,9552,9572,9552,9552,9552,9552,9552,9552,9552,9574,9552,9552,9552,9552,9552,9552,9552,9572,9552,9552,9552,9552,9552,9552,9552,9572,9552,9552,9552,9552,9552,9552,9552,9574,9552,9552,9552,9552,9552,9552,9552,9572,9552,9552,9552,9552,9552,9552,9552,9572,9552,9552,9552,9552,9552,9552,9552,9559],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9568,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9580,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9580,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9571],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9568,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9580,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9580,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9578,9552,9552,9552,9552,9552,9552,9552,9571],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9567,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9579,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9532,9472,9472,9472,9472,9472,9472,9472,9570],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9474, 32 , 32 , 32 , 32 , 32 , 32 , 32 ,9553],
            [9562,9552,9552,9552,9552,9552,9552,9552,9575,9552,9552,9552,9552,9552,9552,9552,9575,9552,9552,9552,9552,9552,9552,9552,9577,9552,9552,9552,9552,9552,9552,9552,9575,9552,9552,9552,9552,9552,9552,9552,9575,9552,9552,9552,9552,9552,9552,9552,9577,9552,9552,9552,9552,9552,9552,9552,9575,9552,9552,9552,9552,9552,9552,9552,9575,9552,9552,9552,9552,9552,9552,9552,9565],
            ]
    
    
    def __init__ (self, sudoku = None):
        if sudoku:
            self.sudoku = np.array(sudoku)
        else:
            pass #Function to input custom sudoku
        
        self.poss = np.empty(0)
    
    
    def __str__ (self):
        boxes = self.boxes_small
        #Substitute numbers
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j]:
                    boxes[1+i*2][2+j*4] = self.sudoku[i][j] + 48
        
        #Turn into a multi-line string
        state = ''
        for line in boxes:
            state += ''.join([chr(int(i)) for i in line])
            state += '\n'
        return state
    
    
    def str_poss (self):
        '''String representation of the <poss> matrix, in the style of __str__.'''
        boxes = self.boxes_big
        
        n = 3
        offset = {1:(0,0), 2:(2,0), 3:(4,0), 4:(0,1), 5:(2,1), 6:(4,1), 7:(0,2), 8:(2,2), 9:(4,2)}
        
        #Substitute numbers
        for i in range(9):
            for j in range(9):
                lst = deepcopy(self.poss[i,j])
                for value in lst:
                    if not np.isnan(value):
                        x = 4*i + 1 + offset[value][1]
                        y = 8*j + 2 + offset[value][0]
                        boxes[x][y] = value + 48 #+48 because 0 in unicode is 48
        
        #Turn into a multi-line string
        state = '\n'.join([''.join([chr(int(i)) for i in row]) for row in boxes])
        return state
    
    
    def which_quadrant (self, position):
        '''Takes a <position> tuple as input and outputs the quadrant it corresponds to (0-8).'''
        x, y = position
        q = (x//3)*3 + y//3
        return q
    
    
    def get_quadrant (self, array, q):
        '''Returns the quadrant q as a list.'''
        quadrant = [array[i,j] for i in range(9) for j in range(9) if q==self.which_quadrant((i,j))]
        assert len(quadrant) == 9
        return quadrant
    
    
    def insert_quadrant (self, array, quad, q):
        '''Inserts the quadrant in the appropriate position in the sudoku.'''
        assert type(array) == np.ndarray
        for i in range(9):
            for j in range(9):
                if self.which_quadrant((i,j)) == q:
                    array[i,j] = quad.pop(0)
        assert type(array) == np.ndarray
        return array
    
    
    def possibility_space (self):
        '''This function creates <poss>, the matrix that represents all the possible numbers
        for each of the sudoku's positions. It first creates a matrix with all the possibilities,
        and then deletes all numbers that are in the same row, column or quadrant for each position.'''
        base = list(range(1,10))
        self.poss = np.empty((9,9,9))
        
        def remove_values (base, lst):
            for value in lst:
                try: base[value-1] = None
                except: pass
            return base
        
        for i in range(9):
            for j in range(9):
                if self.sudoku[i,j] != None:
                    self.poss[i,j,:] = [None]*9
                else:
                    lst = deepcopy(base)
                    
                    lst = remove_values(lst, self.sudoku[i,:])
                    lst = remove_values(lst, self.sudoku[:,j])
                    q = self.which_quadrant((i,j))
                    lst = remove_values(lst, self.get_quadrant(self.sudoku, q))
                    self.poss[i,j] = deepcopy(lst)
        return self.poss
    
    
    def solved (self):
        '''Checks if the sudoku is solved by looking for None values.'''
        not_num = [type(self.sudoku[i,j])!=int for i in range(9) for j in range(9)]
        solved = all(not_num)
        return solved
    
    
    def consistent (self):
        '''Checks the consistency of the sudoku by looking for repeated numbers in rows, columns
        or quadrants. If <poss> exists, checks that all numbers are present between the sudoku
        and the possibility space.
        If the sudoku is not consistent, an Inconsistent exception will be raised.'''
        
        ##Repeated numbers##
        def repeats (lst):
            '''Check list for duplicates'''
            lst = [item for item in lst if item != None]
            lst_set = set(lst)
            contains_duplicates = not(len(lst) == len(lst_set))
            if contains_duplicates:
                message = 'Duplicate numbers found in the Sudoku.'
                raise Sudoku.Inconsistent(message)
            return False
        
        for i in range(9):
            row = self.sudoku[i,:]
            repeats(row)
        
        for i in range(9):
            column = self.sudoku[:,i]
            repeats(column)
        
        for i in range(9):
            quadrant = self.get_quadrant(self.sudoku, i)
            repeats(quadrant)
        
        ##Missing numbers##
        if self.poss.size == 0: return True
        
        def missing_numbers (lst_sudoku, lst_poss):
            '''Checks if all numbers are present between the sudoku and the possibility space.'''
            correct = set(list(range(1,10)))
            lst_sudoku = [elem for elem in lst_sudoku if elem != None]
            lst_poss = [int(elem) for i in lst_poss for elem in i if not np.isnan(elem)]
            
            numbers = set(lst_sudoku)
            numbers.update(lst_poss)
            
            if numbers != correct:
                message = 'A number cannot be placed in any position.'
                raise Sudoku.Inconsistent(message)
            return False
        
        for i in range(9):
            row = self.sudoku[i,:]
            row_poss = self.poss[i,:]
            missing_numbers(row, row_poss)
        
        for i in range(9):
            column = self.sudoku[:,i]
            column_poss = self.poss[:,i]
            missing_numbers(column, column_poss)
        
        for i in range(9):
            quadrant = self.get_quadrant(self.sudoku, i)
            quadrant_poss = self.get_quadrant(self.poss, i)
            missing_numbers(quadrant, quadrant_poss)
        
        return True
    
    
    def only_value (self):
        '''Finds positions in which only one number is possible, and writes it into the sudoku.'''
        for i in range(9):
            for j in range(9):
                count = 0
                for k in range(9):
                    if not np.isnan(self.poss[i,j,k]):
                        count += 1
                        number = self.poss[i,j,k]
                if count == 1:
                    self.sudoku[i,j] = number
    
    
    def only_position (self):
        '''Finds numbers which have only one possible position, and writes it into the sudoku.
        Searches row, column or quadrant-wise.'''
        def check (lst_sudoku, lst_poss):
            '''Checks if there is a number with a single possible position in the list.'''
            for number in range(1,10):
                count = 0
                for i in range(9):
                    if number in lst_poss[i]:
                        count += 1
                        ind = i
                if count == 1:
                    lst_sudoku[ind] = number
            return lst_sudoku
        
        for i in range(9):
            row = self.sudoku[i,:]
            row_poss = self.poss[i,:]
            row = check (row, row_poss)
            self.sudoku[i,:] = row
        
        for i in range(9):
            column = self.sudoku[:,i]
            column_poss = self.poss[:,i]
            column = check (column, column_poss)
            self.sudoku[:,i] = column
            
        
        for i in range(9):
            quadrant = self.get_quadrant(self.sudoku, i)
            quadrant_poss = self.get_quadrant(self.poss, i)
            quadrant = check (quadrant, quadrant_poss)
            self.sudoku = self.insert_quadrant(self.sudoku, quadrant, i)
    
    
    def aligned_values (self):
        #########################################
        #########FUNCTION EMPTIES POSS###########
        #########################################
        
        '''Searches quadrant-wise for values in which all possible positions fall into
        a row or column.'''
        def delete_numbers (number, row_or_col, idx, q):
            if row_or_col == 'row':
                for i in range(9):
                    if q != self.which_quadrant((idx,i)):
                        self.poss[idx,i,number-1] = np.nan
        
        
        
        
        rows    = [{0,1,2}, {3,4,5}, {6,7,8}]
        columns = [{0,3,6}, {1,4,7}, {2,5,8}]
        
        positions = set()
        for q in range(9):
            quad = self.get_quadrant(self.poss, q)
            for number in range(1,10):
                positions.clear()
                for i in range(9):
                    if number in quad[i]:
                        positions.add(i)
                for i in range(3):
                    if positions.issubset(rows[i]):
                        row_num = i + (q%3)*3
                        delete_numbers(number, 'row', row_num, q)
                    if positions.issubset(columns[i]):
                        column_num = i + (q//3)*3
                        delete_numbers(number, 'column', column_num, q)
        



###REDUCING POSSIBILITY SPACE###
def aligned_values (safe, poss):
    '''This function searches each quadrant for values, for which all possible
    possitions fall into a row or a column, and then removes that value from
    that row or column in other quadrants.'''
    safe = deepcopy(safe)
    poss = deepcopy(poss)
    
    def delete_numbers (poss, col_or_row, i, num, q):
        '''Deletes number <num> from <poss> in column or row <i>.'''
        for j in range(9):
            for k in range(9):
                cond_col = col_or_row == 'column' and k == i and quadrant((j,k)) != q
                cond_row = col_or_row == 'row'    and j == i and quadrant((j,k)) != q
                if cond_col or cond_row:
                    try: poss[j][k].remove(num)
                    except ValueError: continue
        return poss
    
    rows    = [{0,1,2}, {3,4,5}, {6,7,8}]
    columns = [{0,3,6}, {1,4,7}, {2,5,8}]
    
    positions = set()
    for q in range(9):
        quad = quadrant_to_list (poss, q)
        quad_safe = quadrant_to_list (safe, q)
        for num in range(1,10):
            positions.clear()
            if num not in quad_safe:
                for i in range(9):
                    if num in quad[i]:
                        positions.add(i)
                for i in range(3):
                    if positions.issubset(columns[i]):
                        col_num = i + (q%3)*3
                        poss = delete_numbers(poss, 'column', col_num, num, q)
                    if positions.issubset(rows[i]):
                        row_num = i + (q//3)*3
                        poss = delete_numbers(poss, 'row', row_num, num, q)
    return poss


def group_matching (positions):
    '''This fuction gets fed a list of numbers and their possible positions (for
    value_group), or vice-versa (for isolated_values). It then aggregates these lists
    to find sets where amount of positions = amount of numbers, and deletes values
    accordingly.'''
    positions = deepcopy(positions)
    pos_set = set()
    n = len(positions)
    
    non_empty = []
    for i in range(len(positions)):
        if positions[i]: non_empty.append(i)
    
    if non_empty == []: return positions
    
    for i in range(2,n):
        combs = combinations(non_empty, i)
        for comb in combs:
            pos_set.clear()
            for elem in comb:
                for j in positions[elem]:
                    pos_set.add(j)

            if len(pos_set) == len(comb): #grouping detected
                for j in range(n):
                    if j not in comb:
                        for pos in pos_set:
                            try: positions[j].remove(pos)
                            except ValueError: pass
                
                new_positions = deepcopy(positions) #take grouped and non-group values appart
                temp_grouping = []
                comb_ = list(comb)
                comb_.reverse()
                for j in comb_:
                    temp_grouping.append(new_positions.pop(j))
                
                new_positions = list(group_matching(new_positions)) #launch again to catch additional groupings
                
                temp_grouping.reverse() #put all values together again
                for j in comb:
                    new_positions.insert(j, temp_grouping.pop(0))
                return new_positions
    return positions


def value_group (poss):
    '''This function looks within a quadrant/row/column for n numbers that are only
    present in n positions. It then removes these values from the rest of the 
    quadrant/row/column.'''
    poss = deepcopy(poss)
    
    #Rows
    for i in range(9):
        row = poss[i]
        row = group_matching(row)
        
        poss[i] = row
    
    #Columns
    for i in range(9):
        column = [row[i] for row in poss]
        column = group_matching(column)

        for j in range(9):
            row = poss[j]
            row.pop(i)
            row.insert(i,column[j])
            poss[j] = row
    
    #Quadrants
    for i in range(9):
        quad = quadrant_to_list(poss,i)
        quad = group_matching(quad)

        poss = list_to_quadrant(poss,quad,i)
    
    return poss


def isolated_values (poss):
    '''This function looks within a quadrant/row/column for groups of n numbers that
    are the only possibilities in n positions. It then removes these values from the
    rest of the quadrant/row/column.'''
    poss = deepcopy(poss)
    
    def one_to_other (one):
        '''Transforms from numbers:positions to positions:numbers and vice-versa.'''
        other = [[],[],[],[],[],[],[],[],[]]
        for posit in range(9):
            for value in range(1,10):
                if value in one[posit]:
                    other[value-1].append(posit+1)
        return other
    
    #Rows
    for i in range(9):
        row = poss[i]
        row = one_to_other(row)
        row = group_matching(row)
        
        poss[i] = one_to_other(row)
    
    #Columns
    for i in range(9):
        column = [row[i] for row in poss]
        column = one_to_other(column)
        column = group_matching(column)
        column = one_to_other(column)

        for j in range(9):
            row = poss[j]
            row.pop(i)
            row.insert(i,column[j])
            poss[j] = row
    
    #Quadrants
    for i in range(9):
        quad = quadrant_to_list(poss,i)
        quad = one_to_other(quad)
        quad = group_matching(quad)
        quad = one_to_other(quad)

        poss = list_to_quadrant(poss,quad,i)
    
    return poss


def reduce_possibilities (safe, poss):
    '''Wrapper function.'''
    safe = deepcopy(safe)
    poss = deepcopy(poss)
    
    poss = aligned_values (safe, poss)
    poss = value_group (poss)
    poss = isolated_values (poss)
    return poss


###LAST RESORT: RECURSIVE###
def hypothesis (safe, poss, view):
    '''If all else fails, this function will form a low-risk (pick a position with
    the lowest number of possible values) hypothesis and try to solve the sudoku
    from then on. If inconsistencies are found, this function will remove that 
    possibility from <poss> and try with a different hypothesis in the same position.
    If no possible values remain, an <Inconsistent> exception will be raised to be
    caught by the parent hypothesis function call. If the exception is caught by the
    main loop, the Sudoku will be considered unsolvable and the program will end.'''
    safe = deepcopy(safe)
    poss = deepcopy(poss)
    
    min = 9
    x,y = 0,0
#    print(poss)
    for i in range(9):
        for j in range(9):
            if len(poss[i][j]) < min and len(poss[i][j]) > 1:
                min = len(poss[i][j])
                x, y = i, j
    assert len(poss[x][y]) != 0
    
    while len(poss[x][y]) != 0:
        hypothesis = poss[x][y].pop(0)
        sudoku = deepcopy(safe)
        sudoku[x][y] = hypothesis
        try: sudoku = solve (sudoku, view, view)
        except Inconsistent: pass
        if solved(sudoku): return sudoku
    
    raise Inconsistent('The hypothesis method found no consistent possibilities.')


###MAIN SOLVE LOOP###
def solve (safe, view = True, view_poss = False, viewall = False):
    '''Main solve loop. May get recursive calls between solve and hypothesis.'''
    safe = deepcopy(safe)
    poss = possibilities (safe)
    
    while True:
        check_consistency (safe)
        
        if solved(safe): return safe
        
        if view:
            os.system('cls')
            print(state(safe))
            if view_poss:
                print(state_poss(poss))
                wait()
        
        poss = possibilities (safe)
        poss_ =  []
        while poss != poss_:
            poss_ = deepcopy(poss)
            poss = reduce_possibilities (safe, poss)
        
        safe, poss, change = update_values (safe, poss)
        
        if change: continue
        
        print('\nLaunching hypothesis')
        safe = hypothesis (safe, poss, viewall)
        

def launch (sudoku, view, view_poss, view_all):
    try: sudoku = solve(sudoku, view = True, view_poss = True, view_all = True)
    except Inconsistent as e:
        print(e.message)
        wait()
        quit()

    os.system('cls')
    print(state(sudoku))
    print('Sudoku is solved!')
    wait()
    print('Program completed')
    

###PROGRAM EXECUTION###
sudoku = test

view = True
view_poss = True
view_all = True

#launch(sudoku, view, view_poss, view_all)