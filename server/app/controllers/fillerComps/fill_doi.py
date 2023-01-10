import re
import requests
from bs4 import BeautifulSoup
from app.db import db
from app.models.paper import Paper

"""Fill doi"""


def fill_doi(paper: Paper, soup: BeautifulSoup):
    # HOT FIXES
    if paper.issue == '39-2' and paper.no == 2:
        paper.doi = '10.18287/0134-2452-2015-39-2-152-157'
        return
    if paper.issue == '40-4' and paper.no == 12:
        paper.doi = '10.18287/2412-6179-2016-40-4-526-534'
        return
    if paper.issue == '41-4' and paper.no == 3:
        paper.doi = '10.18287/2412-6179-2017-41-4-489-493'
        return
    if paper.issue == '41-4' and paper.no == 5:
        paper.doi = '10.18287/2412-6179-2017-41-4-499-503'
        return
    if paper.issue == '41-4' and paper.no == 6:
        paper.doi = '10.18287/2412-6179-2017-41-4-504-509'
        return
    if paper.issue == '41-4' and paper.no == 7:
        paper.doi = '10.18287/2412-6179-2017-41-4-510-514'
        return
    if paper.issue == '41-4' and paper.no == 8:
        paper.doi = '10.18287/2412-6179-2017-41-4-515-520'
        return
    if paper.issue == '41-4' and paper.no == 9:
        paper.doi = '10.18287/2412-6179-2017-41-4-521-527'
        return
    if paper.issue == '41-4' and paper.no == 10:
        paper.doi = '10.18287/2412-6179-2017-41-4-528-534'
        return
    if paper.issue == '41-4' and paper.no == 12:
        paper.doi = '10.18287/2412-6179-2017-41-4-545-551'
        return
    if paper.issue == '41-4' and paper.no == 16:
        paper.doi = '10.18287/2412-6179-2017-41-4-573-576'
        return
    if paper.issue == '41-4' and paper.no == 19:
        paper.doi = '10.18287/2412-6179-2017-41-4-585-587'
        return

    item = soup.find(lambda tag: tag.name == "p" and '10.18287' in tag.text)

    # HOT FIX
    if item is None:
        item = soup.find(lambda tag: tag.name ==
                         "h1" and '10.18287' in tag.text)

    if item is not None:
        text = item.text.replace('- ', '-')
        doi = re.findall(r'10.18287/[CO\d-]+', text)
        paper.doi = doi[0]

    # print(paper.doi)
    return


"""Test doi"""


def test_doi(paper: Paper):
    # FAILED DOI
    # 39-2 3 404 10.18287/0134-2452-2015-39-2-158-162 # Page not found
    # 39-3 3 404 10.18287/0134-2452-2015-39-3-311
    # 39-4 3 404 10.18287/0134-2452-2015-39-4-459-4618
    # 40-1 10 404 10.18287/2412-6179-2016-40-1-64-73
    # 40-2 7 404 10.18287/2412-6179-2015-40-2-173-178
    # 40-6 19 404 10.18287/2412-6179-2016-40-6-899-906
    # 41-2 10 404 10.18287/2412-6179-2017-41-2-218-226
    # 41-2 17 404 10.18287/2412-6179-2017-41-2-284-290
    # 42-3 21 404 10.18287/2412-6179-2018-42-3-521-522
    # 42-4 13 404 10.18287/2412-6179-2018-42-4-637-656
    # 43-2 18 404 10.18287/2412-6179-2019-43-2-296-303
    # 44-3 20 404 10.18287/2412-6179-CO-624
    # 46-3 17 404 10.18287/2412-6179-CO-1052 # Weird page, not found

    if paper.doi is None:
        return

    r = requests.get(f'http://doi.org/{paper.doi}')
    if r.status_code != 200:
        print(paper.issue, paper.no,  r.status_code, paper.doi)

    return
