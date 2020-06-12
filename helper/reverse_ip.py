import re
import tld
import requests

from helper.general import get_info
from requests.utils import requote_uri as encode

class ReverseIP():

    def __init__(self, site):
        self.site = site
        self.agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'

    def bing(self):
        page, pages = 0, 500
        regex = re.compile(r'\<h2\>\<a href="(.*?)" h=".*?"\>')
        query = encode('ip: {}'.format(get_info(self.site, info = 'ip')))
        found = set()

        while (page <= pages):
            bing_url = 'https://bing.com/search?q=' + query + '&first=' + str(page) + '&form=PORE'
            with requests.get(bing_url, headers = {'user-agent' : self.agent}) as request:
                if request.status_code == 200:
                    same_ip = regex.findall(request.text)
                    for url in same_ip:
                        domain = get_info(url, info = 'domain')
                        found.add(domain)
                else:
                    break
            page += 10

        return list(found)

    def you_get_signal(self):
        url = 'https://domains.yougetsignal.com/domains.php'
        domain = get_info(self.site, info = 'domain')
        post_data = {'remoteAddress' : domain, 'key' : ''}

        with requests.post(url, data = post_data, headers = {'user-agent' : self.agent}) as request:
            if request.status_code == 200:
                json = request.json()
                if json.get('status') == 'Success':
                    fetch_domain = lambda x : x[0]
                    return [fetch_domain(domain) for domain in json.get('domainArray')]
                else:
                    return []
            else:
                return []

    def hacker_target(self):
        url = 'http://api.hackertarget.com/reverseiplookup/'
        domain = get_info(self.site, info = 'domain')
        query_string = {'q' : domain}

        with requests.get(url, params = query_string, headers = {'user-agent' : self.agent}) as request:
            if request.status_code == 200:
                if not ('No DNS' in request.text or 'error' in request.text):
                    return request.text.split('\n')
                else:
                    return []
            else:
                return []
