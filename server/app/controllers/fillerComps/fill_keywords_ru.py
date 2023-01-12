import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper
from app.actions.helper import sstr

"""Fill keywords in Russian"""


def fill_keywords_ru(paper: Paper, soup: BeautifulSoup):
    if paper.title_ru is None:
        return
        
    # Fix unclosed taggs
    items = soup.find_all(lambda tag: tag.name ==
                          "p" and 'Ключевые слова' in tag.text)

    if len(items) > 0:
        item = items[-1]
        text = sstr(item.text, True, True)
        kw = re.findall(r'Ключевые слова\s?:(.*)', text)

        if len(kw) > 0:
            kw = kw[0].replace(';', ',')
            kw = sstr(kw, True, True)

            if paper.title_ru is not None:
                paper.keywords_ru = kw
            else:
                paper.keywords_en = kw
            # print(kw)
        else:
            # print('!!!KW is empty', paper.issue, paper.no)
            pass
    else:
        # print('!!!KW not found', paper.issue, paper.no)
        pass

    return
