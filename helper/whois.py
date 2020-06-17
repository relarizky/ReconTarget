import requests
from bs4 import BeautifulSoup
from helper.general import get_info

def whois_from_hacker_target(site):
    domain = get_info(site, info = 'domain')
    urlapi = 'http://api.hackertarget.com/whois/'

    with requests.get(urlapi, params = {'q' : domain}) as request:
        if request.status_code == 200:
            if 'error input invalid' not in request.text:
                return request.text
            else:
                return None
        else:
            return None


def whois_from_whois_com(site):
    domain = get_info(site, info = 'domain')
    urlapi = 'https://www.whois.com/whois/'

    with requests.get(urlapi + domain) as request:
        if request.status_code == 200:
            if 'domain has not been registered' not in request.text:
                parse = BeautifulSoup(request.text, 'lxml')
                parse = parse.find_all('pre', attrs = {'class' : 'df-raw', 'id' : 'registrarData'})
                return parse[0].get_text()
            else:
                return None
        else:
            return None
