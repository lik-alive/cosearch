import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper
from ..helper import sstr

"""Fill keywords in English"""


def fill_keywords_en(paper: Paper, soup: BeautifulSoup):
    if paper.page_en is None:
        return

    vol = paper.issue[0:paper.issue.index(
        '-')] if '-' in paper.issue else paper.issue
    vol = int(vol)

    # HOT FIXES
    if vol < 15:
        return

    # HOT FIXES
    if vol > 38:
        items = soup.find_all(lambda tag: tag.name ==
                              "p" and 'Keywords' in tag.text)
    else:
        items = soup.find_all(lambda tag: tag.name ==
                              "p" and 'Key words' in tag.text)

    if len(items) > 0:
        item = items[-1]
        text = sstr(item.text, True, True)
        if vol > 38:
            kw = re.findall(r'Keywords\s?:(.*)', text)
        else:
            kw = re.findall(r'Key words\s?:(.*)', text)

        if len(kw) > 0:
            kw = kw[0].replace(';', ',')
            kw = sstr(kw, True, True)

            paper.keywords_en = kw
            # print(kw)
        else:
            print('!!!KW is empty', paper.issue, paper.no)
            pass
    else:
        # print('!!!KW not found', paper.issue, paper.no)
        pass

    return
