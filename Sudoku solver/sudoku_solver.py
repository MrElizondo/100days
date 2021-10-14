'''This program attempts to solve sudokus by applying a sequence of common
human techniques.'''
#Fix check consistency
import os
from copy import deepcopy

class Inconsistent(Exception):
    '''Custom error type to express that the Sudoku is inconsistent.'''
    #Must add message that indicates what triggered the inconsistency.
    def __init__(self, message):
        self.message = message


o = None
test_easy = [[7,9,6,1,4,3,o,5,o],[4,5,o,o,o,o,1,3,o],[o,1,o,7,o,2,o,o,9],[9,3,1,o,o,o,o,o,5],[o,o,o,o,o,o,o,o,o],[5,o,o,o,o,o,4,9,1],[6,o,o,8,o,7,o,2,o],[o,7,8,o,o,o,o,1,4],[o,2,o,4,3,9,7,6,8]]
test = [[1,7,o,o,9,o,3,o,8],[6,o,o,o,1,o,o,o,o],[o,5,4,2,o,o,o,o,6],[o,o,o,4,o,o,6,o,o],[5,o,o,o,7,o,o,o,2],[o,o,7,o,o,2,o,o,o],[8,o,o,o,o,6,7,3,o],[o,o,o,o,4,o,o,o,o],[4,o,6,o,5,o,o,8,1]]

###AUXILIARY FUNCTIONS###
def wait ():
    print()
    os.system('pause')


def quadrant (position):
    '''Simple function that takes a position as a tuple and outputs the quadrant
    number for that position.'''
    x, y = position
    quadrant = (x//3)*3 + y//3
    return quadrant


def quadrant_to_list (poss, q):
    '''Converts a given quadrant from <poss> or <safe> into a list.'''
    x = (q//3)*3
    y = (q %3)*3
    lst = [poss[x+i//3][y+i%3] for i in range(9)]
    return lst


def list_to_quadrant (poss, lst, q):
    '''Converts a given lst into a quadrant form and integrates it into poss.'''
    x = (q//3)*3
    y = (q %3)*3
    for j in range (3):
        poss[x+j][y:y+3] = [lst[(j)*3+i] for i in range(3)]
    return poss


def solved (safe):
    '''Checks if the sudoku is solved.'''
    lst = [item for row in safe for item in row]
    solved = (None not in lst)
    return solved

###SECONDARY FUNCTIONS###
def check_consistency (safe, poss = None):
    '''This function checks <safe> for consistency in quadrants, rows and columns,
    and raises an <Inconsistent> exception if there are two equal numbers in the same
    quadrant, row or column.
    The function then checks <poss> for consistency: no possible numbers for a position,
    no possible position for a number in a quadrant, row or column.
    Returns a boolean value.'''
    
    #####<safe>#####
    def repeats (lst):
        '''Check list for duplicates'''
        lst = [item for item in lst if item != None]
        lst_set = set(lst)
        contains_duplicates = not(len(lst) == len(lst_set))
        if contains_duplicates:
            message = 'Duplicate numbers found in the Sudoku.'
            raise Inconsistent(message)
        return False
    
    for i in range(9):
        row = safe[i]
        repeats(row)
    
    for i in range(9):
        column = [safe[j][i] for j in range(9)]
        repeats(column)
        
    for i in range(9):
        quadrant = quadrant_to_list(safe,i)
        repeats(quadrant)
        
    #####<poss>#####
    if not poss: return True
    
    def missing_numbers (lst_safe, lst_poss):
        '''Check if 1-9 are all present in lst_safe and lst_poss.'''
        correct = set((1,2,3,4,5,6,7,8,9))
        
        num_set = set(lst_safe)
        for i in range(len(lst_poss)): num_set.update(lst_poss[i])
        
        try: numset.remove(None)
        except KeyError: pass
        
        if num_set != correct:
            message = 'A number cannot be placed in any position.'
            raise Inconsistent(message)
        return False
        
    for i in range(9):
        for j in range(9):
            if poss[i][j] == [] and not(safe[i][j]):
                message = 'No possibilities left for one of the positions.'
                raise Inconsistent(message)
    
    for i in range(9):
        row_safe = safe[i]
        row_poss = poss[i]
        missing_numbers(row_safe, row_poss)
    
    for i in range(9):
        column_safe = [safe[j][i] for j in range(9)]
        column_poss = [poss[j][i] for j in range(9)]
        missing_numbers(column_safe, column_poss)
        
    for i in range(9):
        quadrant_safe = quadrant_to_list(safe,i)
        quadrant_poss = quadrant_to_list(poss,i)
        missing_numbers(quadrant_safe, quadrant_poss)
        
    return True


def state (safe):
    '''Outputs the state of the sudoku as a multi-line string.'''
    #Box framework. Yep, tons of manual work.
    boxes = [
        [9556,9552,9552,9552,9572,9552,9552,9552,9572,9552,9552,9552,9574,9552,9552,9552,9572,9552,9552,9552,9572,9552,9552,9552,9574,9552,9552,9552,9572,9552,9552,9552,9572,9552,9552,9552,9559],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9568,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9571],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9568,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9580,9552,9552,9552,9578,9552,9552,9552,9578,9552,9552,9552,9571],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9567,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9579,9472,9472,9472,9532,9472,9472,9472,9532,9472,9472,9472,9570],
        [9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553,32,32,32,9474,32,32,32,9474,32,32,32,9553],
        [9562,9552,9552,9552,9575,9552,9552,9552,9575,9552,9552,9552,9577,9552,9552,9552,9575,9552,9552,9552,9575,9552,9552,9552,9577,9552,9552,9552,9575,9552,9552,9552,9575,9552,9552,9552,9565],
        ]
    
    #Substitute numbers
    for i in range(9):
        for j in range(9):
            if safe[i][j]: boxes[i*2+1][j*4+2] = safe[i][j]+48
            else: boxes[i*2+1][j*4+2] = 32
    
    #Turn into a multi-line string
    state = '\n'.join([''.join([chr(i) for i in row]) for row in boxes])
    return state


def print_state (safe):
    os.system('cls')
    print(state(safe))
    

def possibilities (safe):
    '''This function creates <poss> matrix with a list of possible numbers for each
    position, naively considering the numbers present in the quadrant, row and
    column pertaining to that position. Progressively subtracts numbers from a list.'''
    basic = [1,2,3,4,5,6,7,8,9]
    poss = [[basic for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if safe[i][j]:
                poss[i][j] = []
                value = safe[i][j]
                q = quadrant((i,j))
                quad = deepcopy(quadrant_to_list(poss, q))
                for k in range(9):
                    if value in poss[k][j]:
                        lst = deepcopy(poss[k][j])
                        lst.remove(value)
                        poss[k][j] = lst
                    if value in poss[i][k]:
                        lst = deepcopy(poss[i][k])
                        lst.remove(value)
                        poss[i][k] = lst
                    if value in quad[k]:
                        lst = deepcopy(quad[k])
                        lst.remove(value)
                        quad[k] = lst
                        poss = list_to_quadrant(poss, quad, q)
    return poss

###FINDING VALUES###
def only_value (safe, poss):
    '''This function searches <poss> for positions where there is a single possible
    value, and updates <safe> with those values. Change is True is such positions
    are found, False otherwise.'''
    change = False
    for i in range(9):
        for j in range(9):
            if safe[i][j] == None and len(poss[i][j]) == 1:
                safe[i][j] = poss[i][j][0]
                change = True
    return safe, poss, change


def only_position (safe, poss):
    '''This function looks for values in <poss> that have a single possible position
    in either a quadrant, a row or a column, and sets them on <safe>. Change is
    True is such positions are found, False otherwise.'''
    change = False
    def check (lst_safe, lst_poss):
        change = False
        for value in range(1,10):
            count = 0
            for i in range(9):
                if value in lst_poss[i]: count += 1
            if count == 1:
                for i in range(9):
                    if value in lst_poss[i]: lst_safe[i] = value
                change = True
        return lst_safe, change
    
    for i in range(9):
        row_safe = safe[i]
        row_poss = poss[i]
        lst_safe, change1 = check(row_safe, row_poss)
        safe[i] = lst_safe
    
    for i in range(9):
        column_safe = [safe[j][i] for j in range(9)]
        column_poss = [poss[j][i] for j in range(9)]
        lst_safe, change2 = check(column_safe, column_poss)
        safe = [[lst_safe[j] if k == i else safe[j][k] for k in range(9)] for j in range(9)]
        
    for i in range(9):
        quadrant_safe = quadrant_to_list(safe,i)
        quadrant_poss = quadrant_to_list(poss,i)
        lst_safe, change3 = check(quadrant_safe, quadrant_poss)
        safe = list_to_quadrant(safe, lst_safe, i)
        
    return safe, poss, any([change1, change2, change3])


def update_values (safe, poss):
    safe, poss, change1 = only_value(safe,poss)
    safe, poss, change2 = only_position(safe,poss)
    change = change1 or change2
    return safe, poss, change

###REDUCING POSSIBILITY SPACE###
def aligned_values (poss):#not written
    '''This function searches each quadrant for values, for which all possible
    possitions fall into a row or a column, and then removes that value from
    that row or column in other quadrants.'''
    change = False
    return poss, change

    
def value_group (poss):#not written
    '''This function looks within a quadrant/row/column for n numbers that are only
    present in n positions. It then removes these values from the rest of the 
    quadrant/row/column.'''
    change = False
    return poss, change


def isolated_values (poss):#not written
    '''This function looks within a quadrant/row/column for groups of n numbers that
    are the only possibilities in n positions. It then removes these values from the
    rest of the quadrant/row/column.'''
    change = False
    return poss, change


def mixed_groupings (poss):#not written
    '''This function looks for value groupings along the whole matrix.
    "Groupings" and algorithm for this yet to be defined.'''
    change = False
    return poss, change


def reduce_possibilities (poss):
    '''Wrapper function.'''
    change = True
    while change:
        poss, change1 = aligned_values (poss)
        poss, change2 = value_group (poss)
        poss, change3 = isolated_values (poss)
        poss, change4 = mixed_groupings (poss)
        change = any([change1, change2, change3, change4])
    return poss

###LAST RESORT: RECURSIVE###
def hypothesis (safe, poss):#not tested
    '''If all else fails, this function will form a low-risk (pick a position with
    the lowest number of possible values) hypothesis and try to solve the sudoku
    from then on. If inconsistencies are found, this function will remove that 
    possibility from <poss> and try with a different hypothesis in the same position.
    If no possible values remain, an <Inconsistent> exception will be raised to be
    caught by the parent hypothesis function call. If the exception is caught by the
    main loop, the Sudoku will be considered unsolvable and the program will end.'''
    length = [(len(elem) if elem != None else 9) for row in poss for elem in row if elem != None and len(elem) > 1]
    min = 9
    for elem in length:
        if min > elem: min = elem
    t = length.index(min)
    x = t% 9
    y = t//9
    
    while len(poss[x][y]) != 0:
        hypothesis = poss[x][y].pop(0)
        sudoku = deepcopy(safe)
        sudoku[x][y] = hypothesis
        try: sudoku = solve (sudoku)
        except Inconsistent: continue
        if solved(sudoku): return sudoku
    
    raise Inconsistent('The hypothesis method found no consistent possibilities.')

    #Launch solve loop with first guess, delete first guess
    #If exception, repeat
    #If no possibilities are left, raise exception
    
    return safe

###MAIN SOLVE LOOP###
def solve (safe, view = False):
    '''Main solve loop. May get recursive calls between solve and hypothesis.'''
    while True:
        check_consistency (safe)
        if view:
            print_state (safe)
            wait()
        
        poss = possibilities (safe)
        poss = reduce_possibilities (poss)
        
        safe, poss, change = update_values (safe, poss)
        if solved(safe): return safe
        elif change: continue
        
        #safe = hypothesis (safe, poss)
        

def launch (sudoku):
    print_state(sudoku)
    try: sudoku = solve(sudoku, view = False)
    except Inconsistent as e:
        print(e.message)
        wait()
        quit()
        
    print_state(sudoku)
    print('Sudoku is solved!')
    wait()
    

launch(test_easy)