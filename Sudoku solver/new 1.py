from sudoku_solver import *

sudoku = [[1,7,2,6,9,o,3,o,8],
          [6,o,o,o,1,o,o,2,o],
          [o,5,4,2,o,o,o,o,6],
          [2,o,o,4,o,o,6,o,o],
          [5,6,o,o,7,o,o,o,2],
          [o,4,7,o,6,2,o,o,o],
          [8,o,5,o,2,6,7,3,4],
          [7,o,o,o,4,o,o,6,o],
          [4,o,6,o,5,o,o,8,1]]


sudoku = Sudoku(sudoku)
print(sudoku)
sudoku.possibility_space()
sudoku.consistent()
sudoku.str_poss()
sudoku.aligned_values()
print(sudoku.str_poss())
print('Sudoku solved?', sudoku.solved())
print('Sudoku consistent?', sudoku.consistent())
sudoku.only_value()
sudoku.only_position()
print(sudoku)