import re
import tld
import requests

from flask import flash
from helper.general import get_info
from requests.utils import requote_uri as encode

class ReverseIP():

    def __init__(self, site):
        self.site = site
        self.agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'

    def bing(self):
        page, pages = 0, 300
        query = encode('ip: {}'.format(get_info(self.site, 'ip')))
        regex = re.compile(r'\<h2\>\<a href="(.*?)" h=".*?"\>')
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
        pass

    def hacker_target(self):
        pass

    def view_dns(self):
        pass
