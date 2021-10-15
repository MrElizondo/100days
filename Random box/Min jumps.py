#Min jumps function

'''Problem description:
Given an array of integers where each element represents the max number of steps that
can be made forward from that element. Write a function to return the minimum number of
jumps to reach the end of the array (starting from the first element). If an element is 0,
they cannot move through that element. If the end isn’t reachable, return -1.'''


def minjumps (arr):
    '''This approach maps how many jumps you need to reach every position in the array. To do
    this, at every step you calculate which available position has the longest reach for the 
    next jump.'''
    
    #Be in arr[i]. Scan the next <arr[i]> to find the max (j + arr[j]). Mark its position = k.
    #Substitute the values up to position k with the current number of steps.
    #Repeat starting with arr[k].
    if len(arr) == 1: return 0
    
    curr_pos = 0
    step = 0
    
    while True:
        curr_steps = arr[curr_pos]
        
        if curr_pos + curr_steps >= len(arr)-1: return step + 1
        
        max_reach = 0
        max_reach_pos = 0
        for i in range(1,curr_steps+1):
            reach = i + arr[curr_pos + i]
            if reach > max_reach:
                max_reach = reach
                max_reach_pos = i
                
        if max_reach == 0: return -1
        
        step += 1
        curr_pos += max_reach_pos


name = 'Null case'
case = [0]
result = 0
print('OK:', name) if minjumps(case) == result else print('NOK:', name)

name = 'Unreachable case'
case = [1,0,1]
result = -1
print('OK:', name) if minjumps(case) == result else print('NOK:', name)

name = 'Trivial case'
case = [1]
result = 0
print('OK:', name) if minjumps(case) == result else print('NOK:', name)

name = 'Case 1'
case = [1,3,5,8,9,2,6,7,6,8,9]
result = 3
print('OK:', name) if minjumps(case) == result else print('NOK:', name)

name = 'Case 2'
case = [1,1,1,1,1,1,1,1,1,1,1]
result = 10
print('OK:', name) if minjumps(case) == result else print('NOK:', name)