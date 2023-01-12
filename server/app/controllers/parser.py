from app.controllers.parserComps.issue import Issue
from app.db import db
from app.models.paper import Paper
from sqlalchemy.orm import sessionmaker
from .parserComps.parse_issues import parse_issues
from .parserComps.parse_paper_list import parse_paper_list
from .parserComps.parse_paper_no import parse_paper_no
from .parserComps.parse_paper_pdf import parse_paper_pdf
from .parserComps.parse_paper_page_ru import parse_paper_page_ru
from .parserComps.parse_paper_title_and_authors_ru import parse_paper_title_and_authors_ru


class Parser:
    """Html parser."""

    @staticmethod
    def parse():
        db.session.execute('''TRUNCATE TABLE papers''')
        db.session.commit()

        issues = parse_issues('http://computeroptics.ru/KO/KOindex.html')

        startVol = 0  # 0
        startNo = 0  # 0
        endVol = 50  # 50
        endNo = 50  # 50

        if issues is not None:
            for issue in issues:
                if (issue.vol < startVol or (issue.vol == startVol and issue.no < startNo)):
                    continue
                if (issue.vol > endVol or (issue.vol == endVol and issue.no > endNo)):
                    continue

                print(f'issue: {issue.title}')
                Parser.parseIssue(issue)

        db.session.commit()
        db.session.close()
        return 'Success'

    """Parse papers of an issue"""
    @staticmethod
    def parseIssue(issue):
        infos = parse_paper_list(issue)
        for info in infos:
            parse_paper_no(info)
            parse_paper_title_and_authors_ru(info)
            parse_paper_page_ru(info)
            parse_paper_pdf(info)

            # print(info.page_ru, info.page_en)

            paper = Paper(no=info.no,
                          title_ru=info.title_ru,
                          authors_ru=info.authors_ru,
                          title_en=info.title_en,
                          authors_en=info.authors_en,
                          page_ru=info.page_ru,
                          page_en=info.page_en,
                          issue=info.issue,
                          pdf=info.pdf)
            db.session.add(paper)
