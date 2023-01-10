import re
import requests
from bs4 import BeautifulSoup
from .info import Info

"""Parse paper pdf."""


def parse_paper_pdf(info: Info):
    pdf = None
    links = None

    if info.pdf_td is not None:
        links = info.pdf_td.select('a')
    elif info._issue.vol > 18 and info._issue.vol < 25:
        links = info.info_td.select('a')

    if links is not None and len(links) > 0:
        pdf = links[0]['href'] if len(links) > 0 else None

        if '../../../' in pdf:
            pdf = pdf[pdf.index('KO/')+3:]
            pdf = f'http://computeroptics.ru/KO/{pdf}'
        else:
            pdf = f'http://computeroptics.ru/KO/{pdf}'

    info.pdf = pdf

    # HOT FIXES    
    if info.issue == '31-2' and pdf is not None and 'Treb31' in pdf:
        info.pdf = None
    if info.issue == '29' and pdf is not None and 'Treb29' in pdf:
        info.pdf = None

    # print(pdf)

    return 1
