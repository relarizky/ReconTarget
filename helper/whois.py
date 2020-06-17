import re
import requests
from helper.general import get_info

def whois_from_hacker_target(site):
    domain = get_info(site, info = 'domain')
    urlapi = 'http://api.hackertarget.com/whois/'

    with requests.get(urlapi, params = {'q' : domain}) as request:
        if request.status_code == 200:
            return request.text
        else:
            return None


def whois_from_whois_com(site):
    domain = get_info(site, info = 'domain')
    urlapi = 'https://www.whois.com/whois/'

    with requests.get(urlapi + domain) as request:
        if request.status_code == 200:
            pass
        else:
            pass
