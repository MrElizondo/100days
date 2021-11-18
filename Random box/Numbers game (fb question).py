import os

while True:
    total = 0
    
    os.system('cls')
    
    while total < 20:
        while True:
            try:
                num_human = int(input('Enter a number between 1 and 3: '))
                if num_human <= 3 and num_human >= 1:
                    break
            except: pass
            print("That's not a valid number.")
        total += num_human
        print(f'The count is now {total}.\n')
        if total == 20:
            print('You win!')
            break
        
        
        num_machine = 4 - num_human
        total += num_machine
        print(f'The machine chooses the number {num_machine}.')
        print(f'The count is now {total}.\n')
        
        if total == 20:
            print('Machine wins!')
            break
    
    while True:
        ans = input('Would you like to play again? (Y/N)')
        if ans.upper() == 'Y':
            break
        elif ans.upper() == 'N':
            quit()
        else:
            print("That's not a valid answer.")
            continue