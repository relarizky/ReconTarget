import re
import requests
from helper.general import *

def find_link_manual(site):
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    regex = re.compile(r'(href|src|action)="(.*?)"', re.IGNORECASE)


def find_link_hacker_target(site):
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    domain = get_info(site, info = 'domain')
