import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper
from ..helper import sstr

"""Fill abstract in English"""


def fill_abstract_en(paper: Paper, soup: BeautifulSoup):
    if paper.page_en is None:
        return

    vol = paper.issue[0:paper.issue.index(
        '-')] if '-' in paper.issue else paper.issue
    vol = int(vol)

    # HOT FIXES (not done yet)
    if paper.issue == '2' or paper.issue == '5' or paper.issue == '12' or paper.issue == '13' or paper.issue == '14-15_1' or paper.issue == '14-15_2':
        return

    # Fix unclosed taggs
    items = soup.find_all(lambda tag: tag.name ==
                          "p" and 'Abstract' in tag.text)

    if len(items) > 0:
        item = items[-1]

        text = sstr(item.text)
        abstract = re.findall(r'Abstract\s?:(.*)', text)

        # # HOT FIXES
        if (paper.issue == '34-2' and paper.no == 14) or (paper.issue == '35-1' and paper.no == 13) or (paper.issue == '39-1' and paper.no == 2) or (paper.issue == '40-5' and paper.no >= 12 and paper.no <= 20) or (paper.issue == '46-1' and paper.no == 8):
            item = item.find_next_sibling('p')
            abstract = sstr(item.text)

        if len(abstract) > 0:
            abstract = abstract[0]
            abstract = sstr(abstract)

            paper.abstract_en = abstract
            if len(abstract) == 0:
                print('!!!Abstract is empty', paper.issue,
                      paper.no, paper.title_ru)

            # print(len(abstract), paper.issue, paper.no)
        else:
            print('!!!Abstract is empty', paper.issue, paper.no, paper.title_ru)
            pass
    else:
        # print('!!!Abstract not found', paper.issue, paper.no, paper.title_ru)
        pass

    return
