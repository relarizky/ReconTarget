import requests
from bs4 import BeautifulSoup
from helper.general import get_info

def whois_from_hacker_target(site):
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    domain = get_info(site, info = 'domain')
    urlapi = 'http://api.hackertarget.com/whois/?q='

    with requests.get(urlapi + domain, headers = {'user-agent' : agent}) as request:
        if request.status_code == 200:
            if 'error input invalid' not in request.text:
                return request.text
            else:
                return None
        else:
            return None


def whois_from_whois_com(site):
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    domain = get_info(site, info = 'domain')
    urlapi = 'https://www.whois.com/whois/'

    with requests.get(urlapi + domain, headers = {'user-agent' : agent}) as request:
        if request.status_code == 200:
            if 'domain has not been registered' not in request.text:
                parse = BeautifulSoup(request.text, 'html.parser')
                parse = parse.find_all('pre', attrs = {'class' : 'df-raw'})
                return parse[0].get_text()
            else:
                return None
        else:
            return None
