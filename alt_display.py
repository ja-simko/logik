from termcolor import colored
import os
import json
import time
import itertools
from import_gs import import_gsetts, generate_zip


def read_internal_file(file):
    with open(file) as f:
        data = f.read()    
        data = json.loads(data)
    return data

def display(first, game_list=None, guesses=None, hints=None, file='colors.txt', solution=False, win=True):

    def display_header_hints():
        print('',end='\t')
        print(colored('Correct position and color: ■', hint_c[0]),end=' ')
        print(colored('Correct color: ■', hint_c[1]))

    def display_header(hint_bol = True):
        print(colored('GUESSES\t\t\tHINTS','black',attrs=['bold', 'underline']))
        for k,v in valid_mapping.items():
            if v-1 == (len(valid_mapping)+1)//2 and v >= 4:
                hint_bol = False
                display_header_hints()
            print(colored(k.upper()+':'+str(v),game_c[k]),end=' ')
        if hint_bol:
            display_header_hints()
        print('')

    def display_game():
        for count, row in enumerate(guesses):
            for clr_letter in row:
                color_word = game_c[clr_letter]
                print(colored('⬤ ',color_word),end=' ')
            print('\t\t',end='')
            for clr_num in hints[count]:
                print(colored('■ ',hint_c[clr_num]),end=' ')
            print('')
        for i in range(size_set):    
            print(colored('⬤ ','grey'),end=' ')
        if solution:
            print('')
            for i in game_list:
                print(colored('⬤ ',game_c[i]),end=' ')
            return 
        print('')

    def display_solution():
        for i in game_list:
            print(colored('⬤ ',game_c[i]),end=' ')
        return 

    game_settings, size_set, num_of_colors, attempts, extra_atts,  record_max_atts = import_gsetts('game_settings.txt')

    letters_mapped_numbers, letters = generate_zip(num_of_colors)

    data = read_internal_file(file)
    game_c = data['game']
    hint_c = data['hint'] 

    valid_mapping = dict(itertools.islice(letters_mapped_numbers.items(),num_of_colors))

    if solution:
        if not win:
            display_header()
            display_game()
            print(f'\n\t\tBetter luck next time. The solution was:',end=' ')
        display_solution()
        return
    
    os.system('cls')

    display_header()
    if not first:
        display_game()
    else:
        for i in range(size_set):
            print(colored('⬤ ','black'),end=' ')
    print('')



    