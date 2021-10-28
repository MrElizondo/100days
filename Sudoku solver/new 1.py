from sudoku_solver import *

line = [[], [], [2], [5, 6], [], [4, 5], [], [2, 4, 5], []]

line, _ = group_matching(line)

print(line)