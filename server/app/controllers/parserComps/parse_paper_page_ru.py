import re
import requests
from bs4 import BeautifulSoup
from .info import Info

"""Parse paper ru pages"""


def parse_paper_page_ru(info: Info):
    links = info.info_td.select('a')
    for link in links:
        if 'Annot' in link['href'] or 'annot' in link['href'] or 'TEXT' in link['href']:
            # Get ru page
            url = link['href']
            if info.issue == '40-5':
                info.page_en = f'http://computeroptics.ru/KO/ENG/{url}'
            else:
                info.page_ru = f'http://computeroptics.ru/KO/{url}'

            # HOT FIXES
            if info.issue == '42-2' and info.no == 4:
                info.page_ru = f'http://computeroptics.ru/KO/Annot/KO42-2/420204.html'
            if info.issue == '42-2' and info.no == 1:
                info.page_ru = f'http://computeroptics.ru/KO/Annot/KO42-2/420201.html'
            if info.issue == '36-1' and info.no == 14:
                info.page_ru = f'http://computeroptics.ru/KO/Annot/KO36-1/14.html'
            if info.issue == '35-4' and info.no == 16:
                info.page_ru = f'http://computeroptics.ru/KO/Annot/KO35-4/16.html'
            if info.issue == '35-4' and info.no == 4:
                info.page_ru = f'http://computeroptics.ru/KO/Annot/KO35-4/04.html'
            if info.issue == '31-1' and info.no == 7:
                info.page_ru = f'http://computeroptics.ru/KO/Annot/KO31-1/310107.html'

            return

    # print(info.no, 'Ru page not found')
    return
