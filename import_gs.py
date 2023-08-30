import json
import itertools

def read_internal_file(file):
    with open(file) as f:
        data = f.read()    
        data = json.loads(data)
    return data

def import_gsetts(f):
    data = read_internal_file(f)
    game_settings = data[f[:-4]]
    cur_size_set = game_settings['size_set'][0]
    cur_num_of_colors = game_settings['num_colors'][0]
    cur_attempts = game_settings['attempts'][0]
    cur_extra_atts = game_settings['extra_attempts'][0]

    record_max_atts = data['records']['record_max_attempts']
    return game_settings, cur_size_set, cur_num_of_colors, cur_attempts, cur_extra_atts,  record_max_atts

def generate_zip(num_of_colors):
    data = read_internal_file('colors.txt')
    colors_let_name = data['game'] 
    letters = [i for i in colors_let_name]
    letters_mapped_numbers_all = dict(zip(letters,list(range(1,len(letters)+1))))
    valid_mapping = dict(itertools.islice(letters_mapped_numbers_all.items(),num_of_colors))
    return valid_mapping, letters