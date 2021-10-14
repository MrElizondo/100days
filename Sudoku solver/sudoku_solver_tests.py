import sudoku_solver

o = None
test_incomplete_1   = [[1,7,o,o,9,o,3,o,8],[6,o,o,o,1,o,o,o,o],[o,5,4,2,o,o,o,o,6],[o,o,o,4,o,o,6,o,o],[5,o,o,o,7,o,o,o,2],[o,o,7,o,o,2,o,o,o],[8,o,o,o,o,6,7,3,o],[o,o,o,o,4,o,o,o,o],[4,o,6,o,5,o,o,8,1]]
test_incomplete_2   = [[o,6,3,7,o,4,o,o,o],[8,o,o,o,o,o,o,o,o],[4,o,7,1,8,o,5,o,o],[o,o,9,o,o,o,o,3,1],[o,o,8,o,o,o,2,o,o],[2,7,o,o,o,o,9,o,o],[o,o,2,o,3,7,8,o,5],[o,o,o,o,o,o,o,o,6],[o,o,o,2,o,5,3,7,o]]
test_complete_1     = [[1,7,3,9,4,2,8,5,6],[5,2,8,1,6,7,4,3,9],[4,6,9,3,5,8,7,1,2],[2,3,1,7,9,5,6,8,4],[7,4,6,2,8,1,3,9,5],[9,8,5,4,3,6,2,7,1],[3,5,7,6,1,4,9,2,8],[8,9,4,5,2,3,1,6,7],[6,1,2,8,7,9,5,4,3]]
test_inconsistent_1 = [[1,7,3,9,4,2,8,5,6],[5,2,8,1,6,7,4,3,9],[4,6,9,3,5,8,7,1,2],[2,3,1,7,9,5,6,8,4],[7,4,6,2,8,1,3,9,5],[9,8,5,2,3,6,2,7,1],[3,5,7,6,1,4,9,2,8],[8,9,4,5,2,3,1,6,7],[6,1,2,8,7,9,5,4,3]]
test_inconsistent_2 = [[o,6,3,7,o,4,o,o,o],[8,o,o,o,o,o,o,o,o],[4,o,7,1,8,o,5,o,o],[o,o,9,o,o,o,o,3,1],[o,o,8,o,o,o,2,o,o],[2,7,o,o,o,o,9,o,o],[o,6,2,o,3,7,8,o,5],[o,o,o,o,o,o,o,o,6],[o,o,o,2,o,5,3,7,o]]

test_cases = [test_incomplete_1, test_incomplete_2, test_complete_1, test_inconsistent_1, test_inconsistent_2]
test_consistent = [1,1,1,0,0]

def test_state (test_cases):
    success = 0
    errors = []
    for case in test_cases:
        try:
            state = sudoku_solver.state(case)
            assert len(state) == 721
            assert 'None' not in state
            '...'
            success += 1
        except Exception as e: errors.append(e.message)
    result = 'Testing <state> function. '
    result += str(success) + '/' + str(len(test_cases)) + ' tests passed.'
    return result, errors

def test_check_consistency (test_cases, test_consistent):
    #Must include poss testing as well
    success = 0
    errors = []
    for i in range(len(test_cases)):
        try:
            try:
                consistent = sudoku_solver.check_consistency(test_cases[i])
            except sudoku_solver.Inconsistent:
                consistent = False
            print(consistent)
            assert consistent == bool(consistent)
            assert consistent == bool(test_consistent[i])
            
            success += 1
        except AssertionError: errors.append('Asertion error.')
        except Exception as e: errors.append(e.message)
    result = 'Testing <check_consistency> function. '
    result += str(success) + '/' + str(len(test_cases)) + ' tests passed.'
    return result, errors

print([sudoku_solver.solved(case) for case in test_cases])
#result, errors = test_state(test_cases)
#result, errors = test_check_consistency(test_cases, test_consistent)

print(result)
print('Errors: ', end='')
if len(errors) == 0: print('None')
else:
    print()
    for error in errors:
        print('   ' + error)