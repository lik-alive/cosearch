import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper
from app.actions.helper import sstr

"""Fill paper page in English"""


def fill_page_en(paper: Paper):
    if paper.page_ru is None:
        return

    # HOT FIXES (not done yet)
    if paper.issue == '2' or paper.issue == '5' or paper.issue == '12' or paper.issue == '13' or paper.issue == '14-15_1' or paper.issue == '14-15_2':
        return

    page = paper.page_ru
    page = page.replace('/KO/', '/eng/KO/')

    # HOT FIXES
    vol = paper.issue[0:paper.issue.index(
        '-')] if '-' in paper.issue else paper.issue
    vol = int(vol)
    if paper.issue == '42-5':
        page = page.replace('/4204', '/4205')
    elif paper.issue == '38-4':
        page = page.replace('/3804', '/3803')
    elif paper.issue == '38-2' and paper.no >= 20 and paper.no <= 27:
        page = page.replace('/38021', '/3802')
    elif paper.issue == '38-1':
        page = page.replace('/3801', '/')
    elif paper.issue == '37-4':
        page = page.replace('/3704', '/')
    elif paper.issue == '35-1':
        page = page.replace('KO35-1/', 'KO35-1/3501')
    elif paper.issue == '34-4':
        page = page.replace('KO34-4/', 'KO34-4/3404')
    elif paper.issue == '33-4' and paper.no != 1:
        page = page.replace('KO33-4/', 'KO33-4/3304')
    elif paper.issue == '33-3':
        page = page.replace('KO33-3/', 'KO33-3/3303')
    elif paper.issue == '33-2':
        page = page.replace('KO33-2/', 'KO33-2/3302')
    elif paper.issue == '31-4':
        page = page.replace('KO31-4/', 'KO31-4/3104')
    elif paper.issue == '31-3':
        page = page.replace('KO31-3/', 'KO31-3/3103')
    elif paper.issue == '1':
        page = page.replace('/eng/KO/', '/eng/KO/ENG/')
        page = page.replace('Annot/KO01/', 'annot/KO_01/')
    elif paper.issue == '3':
        page = page.replace('/eng/KO/', '/eng/KO/ENG/')
        page = page.replace('Annot/KO03/', 'annot/KO_02_1/')
    elif paper.issue == '4':
        page = page.replace('/eng/KO/', '/eng/KO/ENG/')
        page = page.replace('Annot/KO04/', 'annot/KO_02_2/')
    elif vol >= 43 and paper.issue != '43-1' and paper.issue != '43-2':
        page = page.replace('.html', 'e.html')

    r = requests.get(page)
    if r.status_code != 200:
        paper.page_en = None
        print(paper.issue, paper.no, r.status_code, page)
    else:
        paper.page_en = page

    return
