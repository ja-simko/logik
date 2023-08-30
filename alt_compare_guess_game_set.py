import time
def compare_sets(guess_list, game_list, agg_hints):
    hints = list()
    def color_and_position():
        game_list_mod = game_list.copy()
        guess_list_mod = guess_list.copy()
        for pos,letter in enumerate(guess_list):
            if letter == game_list[pos]:
                hints.append(0)
                game_list_mod[pos] = 0
                guess_list_mod[pos] = 0
        return game_list_mod, guess_list_mod, hints

    def only_color(game_list, guess_list,hints):
        for letter in guess_list:
            if letter != 0 and letter in game_list:
                place = game_list.index(letter)
                game_list[place] = 0
                hints.append(1)
        return hints  
    
    game_list_mod, guess_list_mod, hints = color_and_position()
    hints = only_color(game_list_mod, guess_list_mod, hints)
    agg_hints.append(hints)
    return agg_hints