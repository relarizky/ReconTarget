from requests import get
from helper.general import get_info

def dns_lookup_hacker_target(site):
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    domain = get_info(site, info = 'domain')
    urlapi = 'http://api.hackertarget.com/dnslookup/'

    with get(urlapi, params = {'q' : domain}, headers = {'user-agent' : agent}) as request:
        if request.status_code == 200:
            if 'error input invalid' not in request.text:
                return request.text
            else:
                return None
        else:
            return None
