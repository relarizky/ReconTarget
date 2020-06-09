import os
import json
import requests

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


def text_date(value):
    months = {
        1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April',
        5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August',
        9 : 'September', 10 : 'October', 11 : 'November', 12 : 'December'
    }
    year, month, date = str(value).split('-')
    date = date.replace('0', '')
    month = month.replace('0', '')
    month = months[int(month)]
    return '{} {}, {}'.format(month, date, year)


def get_status_code(url): # for checking connection
    header = {'user-agent' : 'Mozilla/5.0'}
    with requests.get(url, headers = header) as request:
        return request.status_code
