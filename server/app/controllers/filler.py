import re
import requests
from bs4 import BeautifulSoup
from flask import jsonify
from app.controllers.parserComps.issue import Issue
from app.db import db
from app.models.paper import Paper
from .fillerComps.fill_doi import fill_doi
from .fillerComps.fill_doi import test_doi
from .fillerComps.fill_keywords_ru import fill_keywords_ru
from .fillerComps.fill_citation_ru import fill_citation_ru
from .fillerComps.fill_abstract_ru import fill_abstract_ru
from .fillerComps.fill_page_en import fill_page_en
from .fillerComps.fill_keywords_en import fill_keywords_en
from .fillerComps.fill_citation_en import fill_citation_en
from .fillerComps.fill_abstract_en import fill_abstract_en
from .parserComps.parse_issues import parse_issues
from .parserComps.parse_paper_list import parse_paper_list
from .parserComps.parse_paper_no import parse_paper_no
from .parserComps.parse_paper_title_and_authors_en import parse_paper_title_and_authors_en
from .parserComps.parse_paper_title_and_authors_ru import parse_paper_title_and_authors_ru
from sqlalchemy.sql.expression import func


class Filler:
    """Paper info filler."""

    @staticmethod
    def fill_base_en():
        # Fill page_en link
        for paper in db.session.query(Paper).all():
            fill_page_en(paper)

            if paper.id % 100 == 0:
                print(f'paper: {paper.id}')

        # Fill english title and authors
        issues = parse_issues('http://computeroptics.ru/KO/KOindex.html')

        for issue in issues:
            if issue.ru_href is None:
                continue

            # if not (issue.vol >= 47 and issue.vol <= 50):
            #     continue

            print(f'issue: {issue.title}')

            infos = parse_paper_list(issue, True)

            for info in infos:
                parse_paper_no(info)
                parse_paper_title_and_authors_en(info)

                if info.no is not None:
                    paper = db.session.query(Paper).filter(
                        Paper.issue == info.issue).filter(Paper.no == info.no).first()

                    if paper is not None:
                        paper.authors_en = info.authors_en
                        paper.title_en = info.title_en
                    else:
                        print("!!!Paper not found", info.issue, info.no)

        # HOT FIXES
        paper = db.session.query(Paper).filter(Paper.issue == "1").filter(
            Paper.authors_ru.like("%Велихов%")).first()
        paper.title_en = "Foreword"
        paper = db.session.query(Paper).filter(Paper.issue == "1").filter(
            Paper.authors_ru.like("%Прохоров%")).first()
        paper.title_en = "Foreword"
        paper = db.session.query(Paper).filter(Paper.issue == "37-4").filter(
            Paper.title_ru.like("%Боброва%")).first()
        paper.title_en = "In the memory of Sergei Timofeevich Bobrov"
        paper = db.session.query(Paper).filter(Paper.issue == "45-4").filter(
            Paper.title_ru.like("%От редакции%")).first()
        paper.title_en = "Editorial: The hundredth issue of the journal Computer Optics"

        db.session.commit()
        db.session.close()
        return 'Success'

    @staticmethod
    def fill_data_ru():
        # for paper in db.session.query(Paper).filter(Paper.issue.like("%44-5%")).all(): #34-2(14) 35-1(13) 39-1(2) 40-5(12-20)
        for paper in db.session.query(Paper).all():
            if paper.page_ru is None:
                continue

            r = requests.get(paper.page_ru)
            soup = BeautifulSoup(r.content, 'html.parser',
                                 from_encoding="utf8")
            # HOT FIXES
            if paper.issue == '33-3' and (paper.no == 7 or paper.no == 9):
                content = r.content.decode('utf-8').encode('windows-1251',
                                                           errors='ignore').decode('utf-8', errors='ignore').encode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')

            fill_doi(paper, soup)
            fill_keywords_ru(paper, soup)
            fill_citation_ru(paper, soup)
            fill_abstract_ru(paper, soup)
            if paper.id % 100 == 0:
                print(f'paper: {paper.id}')

        db.session.commit()
        db.session.close()
        return 'Success'

    @staticmethod
    def fill_data_en():
        # for paper in db.session.query(Paper).filter(Paper.issue.like("%44-5%")).all(): #34-2(14) 35-1(13) 39-1(2) 40-5(12-20)
        for paper in db.session.query(Paper).all():
            if paper.page_en is None:
                continue

            r = requests.get(paper.page_en)
            soup = BeautifulSoup(r.content, 'html.parser',
                                 from_encoding="utf8")

            if paper.doi is None:
                fill_doi(paper, soup)

            fill_keywords_en(paper, soup)
            fill_citation_en(paper, soup)
            fill_abstract_en(paper, soup)
            if paper.id % 100 == 0:
                print(f'paper: {paper.id}')

        db.session.commit()
        db.session.close()
        return 'Success'

    """Fill in paper years"""
    @staticmethod
    def fill_years():
        for paper in db.session.query(Paper).all():
            vol = paper.issue[0:paper.issue.index(
                '-')] if '-' in paper.issue else paper.issue
            vol = int(vol)

            if vol <= 2:
                year = 1987
            elif vol <= 3:
                year = 1988
            elif vol <= 6:
                year = 1989
            elif vol <= 8:
                year = 1990
            elif vol <= 9:
                year = 1991
            elif vol <= 12:
                year = 1992
            elif vol <= 13:
                year = 1993
            elif vol <= 14:
                year = 1995
            elif vol <= 20:
                year = 1980 + vol
            elif vol <= 22:
                year = 2001
            elif vol <= 24:
                year = 2002
            elif vol <= 25:
                year = 2003
            elif vol <= 26:
                year = 2004
            elif vol <= 28:
                year = 2005
            elif vol <= 30:
                year = 2006
            else:
                year = 2023 - 47 + vol

            paper.year = year

        db.session.commit()
        db.session.close()
        return 'Success'

    """Fix fill errors"""
    @staticmethod
    def fill_data_fix():
        for paper in db.session.query(Paper).filter(Paper.id.in_([2158, 2166, 2157, 2168, 2164, 2163, 2167])).all():
            r = requests.get(paper.page_ru)
            soup = BeautifulSoup(r.content, 'html.parser',
                                 from_encoding="utf8")
            fill_abstract_ru(paper, soup)

        for paper in db.session.query(Paper).filter(Paper.id.in_([1032, 2001, 2000, 2036, 1999])).all():
            r = requests.get(paper.page_en)
            soup = BeautifulSoup(r.content, 'html.parser',
                                 from_encoding="utf8")
            fill_abstract_en(paper, soup)

        for paper in db.session.query(Paper).filter(Paper.title_en == None).filter(Paper.title_ru == None).filter(Paper.pdf.like("%Treb%")).all():
            paper.title_ru = "Правила подготовки рукописей для журнала «Компьютерная оптика»"

        for paper in db.session.query(Paper).filter(Paper.issue == '3').filter(Paper.pdf.like("%avt.pdf%")).all():
            paper.title_ru = 'Правила подготовки рукописей для журнала «Компьютерная оптика»'

        for paper in db.session.query(Paper).filter(Paper.issue == '12').filter(Paper.pdf.like("%an.pdf%")).all():
            paper.title_ru = 'Аннотации'
            paper.title_en = 'Abstracts'

        for paper in db.session.query(Paper).filter(Paper.issue == '31-2').filter(Paper.title_en == None).filter(Paper.title_ru == None).all():
            paper.title_ru = 'Правила подготовки рукописей для журнала «Компьютерная оптика»'

        for paper in db.session.query(Paper).filter(Paper.abstract_en != None).filter(func.length(Paper.abstract_en) < 10).all():
            print(paper.id)
            r = requests.get(paper.page_en)
            soup = BeautifulSoup(r.content, 'html.parser',
                                 from_encoding="utf8")
            fill_abstract_en(paper, soup)

        for paper in db.session.query(Paper).filter(Paper.abstract_ru != None).filter(func.length(Paper.abstract_ru) < 10).all():
            print(paper.id)
            r = requests.get(paper.page_ru)
            soup = BeautifulSoup(r.content, 'html.parser',
                                 from_encoding="utf8")
            # HOT FIXES
            if paper.issue == '33-3' and (paper.no == 7 or paper.no == 9):
                content = r.content.decode('utf-8').encode('windows-1251',
                                                           errors='ignore').decode('utf-8', errors='ignore').encode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')

            fill_abstract_ru(paper, soup)

        db.session.commit()
        db.session.close()
        return 'Success'
