import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper
from ..helper import sstr

"""Fill citation in Russian"""


def fill_citation_ru(paper: Paper, soup: BeautifulSoup):
    if paper.title_ru is None:
        return
    
    # Fix unclosed taggs
    items = soup.find_all(lambda tag: tag.name ==
                          "p" and 'Цитирование' in tag.text)

    if len(items) > 0:
        item = items[-1]
        text = sstr(item.text, True, True)
        citation = re.findall(r'Цитирование\s?:(.*)', text)

        if len(citation) > 0:
            citation = citation[0]
            citation = sstr(citation, True, True)

            paper.citation_ru = citation
            # print(citation)
        else:
            print('!!!Citation is empty', paper.issue, paper.title_ru)
            pass
    else:
        # print('!!!Citation not found', paper.issue, paper.title_ru)
        pass

    return
