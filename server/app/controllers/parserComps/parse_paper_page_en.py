import re
import requests
from bs4 import BeautifulSoup
from .info import Info

"""Parse paper en pages"""


def parse_paper_page_en(info: Info):
    # Get en page
    r = requests.get(info.page_ru)
    soup = BeautifulSoup(r.content, 'html.parser')
    elinks = soup.select('a')
    for elink in elinks:
        if 'English' == elink.text:
            eurl = elink['href']
            eurl.replace('../', '');
            info.page_en = f'http://computeroptics.ru/{eurl}'
            return
        
    print(info.no, 'En page not found')

    return
