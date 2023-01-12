import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper
from app.actions.helper import sstr

"""Fill abstract in Russian"""


def fill_abstract_ru(paper: Paper, soup: BeautifulSoup):
    if paper.title_ru is None:
        return

    # Fix unclosed taggs
    items = soup.find_all(lambda tag: tag.name ==
                          "p" and 'Аннотация' in tag.text)

    if len(items) > 0:
        item = items[-1]

        text = sstr(item.text)
        abstract = re.findall(r'Аннотация\s?:(.*)', text)

        # HOT FIXES
        if (paper.issue == '33-3' and paper.no >= 11 and paper.no <= 14) or (paper.issue == '34-4' and paper.no == 5) or (paper.issue == '35-2' and paper.no == 5) or (paper.issue == '38-1' and paper.no >= 2 and paper.no <= 22) or (paper.issue == '41-6' and paper.no == 23) or (paper.issue == '42-1' and paper.no == 20) or (paper.issue == '43-2' and paper.no >= 17 and paper.no <= 21):
            item = item.find_next_sibling('p')
            abstract = sstr(item.text)

        if len(abstract) > 0:
            abstract = abstract[0]

            # HOT FIXES
            if "электронная почта" in abstract:
                abstract = abstract[0:abstract.index("Ключевые слова")]

            abstract = sstr(abstract)

            paper.abstract_ru = abstract
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
