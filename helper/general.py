import os
import re
import tld
import json
import socket
import requests

from flask import flash
from flask import send_from_directory

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


def check_valid_url(url):
    try:
        check = tld.get_tld(url, as_object = True)
    except (tld.exceptions.TldBadUrl, tld.exceptions.TldDomainNotFound):
        return False
    else:
        return True


def check_connection(url):
    try:
        user_agent = {'user-agent' : 'Mozilla/5.0'}
        request = requests.get(url, headers = user_agent, allow_redirects = True)
        return {
            'url' : request.url,
            'code' : request.status_code,
            'server' : request.headers.get('server') if 'server' in request.headers else '-'
        }
    except requests.exceptions.RequestException as Error:
        flash('error', 'Fail to input URL because, {}'.format(Error))
        return False


def get_country(site):
    domain = tld.get_tld(site, as_object = True)
    ip = socket.gethostbyname(domain.parsed_url.netloc)
    agent = {'user-agent' : 'Mozilla/5.0'}

    with requests.get('https://ipinfo.io/{}/json'.format(ip), headers = agent) as request:
        json = request.json()
        if 'country' not in json:
            return 'unknown'
        else:
            return json.get('country').lower()


def filter_target_form(target_url):
    error = 0

    if len(target_url) == 0:
        flash('error', 'Please fill all the required fields.')
        error += 1
    elif not check_valid_url(target_url):
        flash('error', 'Invalid URL.')
        error += 1
    else:
        if len(target_url) > 50:
            flash('error', 'URL target is too much long.')
            error += 1

    return error == 0


def get_flag_image(country):
    directory = os.getcwd() + '/tool/auth/assets/images/flags/'
    return send_from_directory(directory, filename = country.lower() + '.png')
