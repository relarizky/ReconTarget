import os
import json

def get_config(key):
    config_file = os.getcwd() + '/config.json'
    with open(config_file, 'r') as file:
        config = json.loads(file.read())
        return config[key]


def pascal_case(string):
    capital = lambda text : text.capitalize()
    strings = string.split(' ')
    strings = list(map(capital, strings))
    return ' '.join(strings)


def auto_update():
    pass
