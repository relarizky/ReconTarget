from requests import get
from helper.general import get_info

def dns_lookup_hacker_target(site):
    domain = get_info(site, info = 'domain')
    urlapi = 'http://api.hackertarget.com/dnslookup/'

    with get(urlapi, params = {'q' : domain}) as request:
        if request.status_code == 200:
            if 'error input invalid' not in request.text:
                return request.text
            else:
                return None
        else:
            return None
