import numpy as np
import os
import time
#import game_settings
#import colors
import keyboard
import json
from termcolor import colored
from display import display
from compare_sets import compare_sets
from import_gs import import_gsetts, generate_zip, countdown

def read_internal_file(file):
    with open(file) as f:
        data = f.read()    
        data = json.loads(data)
    return data

def dump_to_file(file, content):
    with open(file, "w") as outfile:
        json.dump(content, outfile,indent=4)

def generate_game_list(set_size, letters_mapped_numbers, game_list=list()):
    game_list = np.random.choice(list(letters_mapped_numbers.keys()), size=set_size)
    game_list = game_list.tolist()
    agg_1 = []
    agg_2 = []
    return game_list, agg_1, agg_2

def go_to_settings():
    data = read_internal_file('game_settings.txt')
    game_settings = data['game_settings']
    print(game_settings)
    abbrev = {'set':'set_size','num':'num_colors','att':'attempts','ext':'extra_attempts'} 
    for k in abbrev:
        print(k,end =' | ')
    option = input("\nSelect what you want to change: ")
    if option in abbrev:
        try:
            value = int(input("Change to value: "))
            full_name = abbrev[option]
            if value > data['game_settings'][full_name][1]:
                print("Too many! Have you lost your marbles?!",end=' ')
                print("The limit is mere "+str(data['game_settings'][full_name][1]))
                countdown(5)
                return
            else:
                data['game_settings'][full_name][0] = value
                dump_to_file('game_settings.txt',data)
                print('We recommend quitting the game to assure everything\'s working properly.')
                countdown(5)
                return
        except:
            print('Not a number.')
            countdown(3)
            return

def welcome_in_game(set_size, num_of_colors):
    os.system('cls')
    commands = ['h','menu','help']
    italic_commands = [colored("\x1B[3m'" + i + "'\x1B[0m","white") for i in commands]
    italic_commands_joined = "; ".join(italic_commands)
    parenthesis = colored(")","light_yellow")
    print(colored(f"WELCOME IN LOGIK, AKA MASTERMIND\n(to see more options, type: {str(italic_commands_joined)}{parenthesis}","light_yellow"))
    display(True)
    letters_mapped_numbers, letters = generate_zip(num_of_colors)
    return commands, letters_mapped_numbers

def get_to_menu():
        while True:
            os.system('cls')
            print('Quit game: q | Settings: s | Escape: Esc')
            keyboard.read_key()
            if keyboard.is_pressed("q"):
                os.system('cls')
                print('You just quit the game!')
                exit()
            if keyboard.is_pressed("s"):
                go_to_settings()
            if keyboard.is_pressed("esc"):
                print("Esc pressed, you are being redirected back to the game!")
                break
            os.system('cls')

def letters_to_integers(guess, letters_mapped_numbers, num_of_colors, warnings):

    data = read_internal_file('colors.txt')
    all_letters_numbers = data['game']

    abc_guess = []
    num_warnings = set()
   
    valid_letters = ["\x1B[3m" + k + "\x1B[0m" for k in letters_mapped_numbers]
    valid_numbers = ["\x1B[3m" + str(i+1) + "\x1B[0m" for i in range(num_of_colors)]
   

    warning_both = warnings['disallowed_input'].format(numbers = ", ".join(valid_numbers), letters = ", ".join(valid_letters))
    for i in guess:
        i = i.lower()
        if i in all_letters_numbers:
            if i in letters_mapped_numbers:
                abc_guess.append(i)
            else:
                num_warnings.add('letter') 
        else:
            try:
                i = int(i)
                if i <= len(letters_mapped_numbers) and i != 0:
                    letter = next(k for k,v in letters_mapped_numbers.items() if v == i)
                    abc_guess.append(letter)
                else:
                    num_warnings.add('number')
            except:
                print(warning_both)
                return None, False
    if len(num_warnings) >= 2:
        print(warning_both)
    else:
        try: 
            if list(num_warnings)[0] == 'letter':
                print(warnings['wrong_letters'].format(valid_letters = ", ".join(valid_letters)))
            else:
                print(warnings['wrong_numbers'].format(num_of_colors = num_of_colors))
        except IndexError:
            return abc_guess, True
    return None, False

def manipulate_input(guess, guess_list):
    guess_list = guess.replace(" ","").replace("",",").split(',')
    guess_list.pop(0)
    guess_list.pop()
    return guess_list

def get_input(commands):
    guess_as_str = input("Your guess: ")
    while guess_as_str in commands:
        get_to_menu()
        guess_as_str = input("Your guess: ")
    return guess_as_str

def check_input(is_valid, num_of_colors, set_size, commands, agg_guesses, letters_mapped_numbers):
    while not is_valid:
        guess_as_str = get_input(commands)
        guess_list = manipulate_input(guess_as_str, guess_list = list())
        data = read_internal_file('warnings.txt')
        if len(guess_list) != set_size:
            print(data["max_size"].format(guess_length = set_size))
            continue
        abc_guess, is_valid= letters_to_integers(guess_list, letters_mapped_numbers, num_of_colors, warnings = data)
    agg_guesses.append(abc_guess)
    return abc_guess, agg_guesses

def end_game(max_attempts,player_attempts, extra, guess, solution):
    player_attempts +=1
    if guess == solution:
        print('Congratulations. The solution is indeed:',end=' ')
        display(False, solution, solution=True)
        return True, player_attempts, max_attempts, True
    if player_attempts != max_attempts:
        return False, player_attempts, max_attempts, False
    else:
        print("You lost, but I can give you three extra attempts.")
        input_yes = input("If you want to continue, type 'y': ")
        if input_yes == 'y':
            max_attempts += extra
            return False, player_attempts, max_attempts, False
        else:
            return True, player_attempts, max_attempts, False
            
def start_the_game():
    player_attempts = 0
    game_settings, set_size, num_of_colors, limit_attempts, extra_attempts, record_max_atts = import_gsetts('game_settings.txt')
    access_menu_commands, letters_mapped_numbers = welcome_in_game(set_size, num_of_colors)
    game_list, agg_guesses, agg_hints = generate_game_list(set_size,letters_mapped_numbers)
    is_end = False
    while not is_end:
        abc_guess_list, agg_guesses = check_input(False, num_of_colors, set_size, access_menu_commands, agg_guesses, letters_mapped_numbers)

        agg_hints = compare_sets(abc_guess_list, game_list, agg_hints)

        display(False, game_list, agg_guesses, agg_hints)
        is_end, player_attempts, limit_attempts, win = end_game(limit_attempts, player_attempts, game_settings['extra_attempts'][0], abc_guess_list, game_list)

        if is_end:
            if not win:
                os.system('cls')
                display(False, game_list, agg_guesses, agg_hints, solution=True, win = False)
            else:
                if player_attempts < record_max_atts:
                    data = read_internal_file('game_settings.txt')
                    record_max_atts = player_attempts
                    data['records']['record_max_attempts'] = record_max_atts
                    dump_to_file('game_settings.txt',data)
                print(f'It took you {player_attempts} attempts. The record is {record_max_atts}.')
                cont = input("Continue ('y')?: ")
                if cont == 'y':
                    start_the_game()

start_the_game()