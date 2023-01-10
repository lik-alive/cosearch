import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper
from ..helper import sstr

"""Fill citation in English"""


def fill_citation_en(paper: Paper, soup: BeautifulSoup):
    if paper.page_en is None:
        return

    vol = paper.issue[0:paper.issue.index(
        '-')] if '-' in paper.issue else paper.issue
    vol = int(vol)

    #HOT FIXES
    if vol < 15 or (vol >= 33 and vol <= 38 and paper.issue != "37-1") or paper.issue == '39-1':
        return

    # Fix unclosed taggs
    items = soup.find_all(lambda tag: tag.name ==
                          "p" and 'Citation' in tag.text)

    if len(items) > 0:
        item = items[-1]
        text = sstr(item.text, True, True)
        citation = re.findall(r'Citation\s?:(.*)', text)

        if len(citation) > 0:
            citation = citation[0]
            citation = sstr(citation, True, True)

            paper.citation_en = citation
            # print(citation)
        else:
            print('!!!Citation is empty', paper.issue, paper.no, paper.title_ru)
            pass
    else:
        # print('!!!Citation not found', paper.issue, paper.no, paper.title_ru)
        pass

    return
