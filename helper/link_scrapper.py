import re
import requests
from helper.general import *

def find_link_manual(site):
    found = []
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    regex = re.compile(r'(href|src|action)="(.*?)"', re.IGNORECASE)
    domain = get_info(site, info = 'domain')

    with requests.get(site, headers = {'user-agent' : agent}) as request:
        if request.status_code == 200:
            found = [url[-1] for url in regex.findall(request.text)]
        else:
            found = []

    remove_none = lambda element : element != ''
    remove_external = lambda element : \
    (not element.startswith(site) and not element.startswith('http')) or domain in element

    found = list(filter(remove_none, found)) # remove none and ''
    found = list(filter(remove_external, found)) # remove third-party link
    found = list(set(found)) # remove duplicate

    return found


def find_link_hacker_target(site):
    found = []
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    domain = get_info(site, info = 'domain')
    urlapi = 'http://api.hackertarget.com/pagelinks/?q='

    with requests.get(urlapi + domain, headers = {'user-agent' : agent}) as request:
        if request.status_code == 200:
            if 'url is invalid' not in request.text:
                found = request.text.split('\n')
            else:
                found = []
        else:
            found = []

    remove_none = lambda element : element != ''
    found = list(set(filter(remove_none, found)))

    return found
