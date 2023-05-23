import os
import re
import requests
from flask import jsonify, request, Response, stream_with_context
from app.actions.translator import Translator
from app.db import db
from app.models.paper import Paper
from sqlalchemy.sql import false
from .scopus import Scopus
from app.log import log


class Searcher:
    """Search for papers."""

    @staticmethod
    def search(type):
        data = request.get_json() or {}

        # No term provided
        if not 'query' in data:
            return "Query is required", 422

        query = data['query']
        isGlobal = '!' in query

        # Too long query
        if len(query) > 255:
            return "Query should not exceed 255 characters", 422

        # Split terms and convert to lower case
        terms = [t.replace('!', '').strip().lower()
                 for t in query.split(',') if len(t.replace('!', '').strip()) >= 3]

        # Minimum - 1 term
        if len(terms) < 1:
            return "Query should contain at least 1 term of minimum 3 characters", 422

        # Maximum - 10 terms
        if len(terms) > 10:
            return "Query should not exceed 10 keywords", 422

        # Separate Russian and English terms
        termsRu = []
        termsEn = []
        for term in terms:
            # Russian term
            if re.search(r'[А-ЯЁа-яё]', term) is not None:
                termsRu.append(term)
            # English term
            else:
                termsEn.append(term)

        # Translate only Russian terms
        if len(termsRu) > 0:
            termsEn += Translator.translate(termsRu, 'en') or []

        if (type == 'scopus'):
            data = Searcher.search_scopus(termsEn)
            log.info(f"Scopus: {query}")
        else:
            data = Searcher.search_co(termsRu, termsEn, isGlobal)
            log.info(f"CO: {query}")

        db.session.close()

        return jsonify(data)

    """Search in Computer Optics"""
    @staticmethod
    def search_co(termsRu, termsEn, isGlobal = False):
        # Create filter
        termFilter = false()
        for term in termsRu:
            termFilter |= Paper.title_ru.like(f"%{term}%") | Paper.keywords_ru.like(
                f"%{term}%") | Paper.abstract_ru.like(f"%{term}%")
        for term in termsEn:
            termFilter |= Paper.title_en.like(f"%{term}%") | Paper.keywords_en.like(
                f"%{term}%") | Paper.abstract_en.like(f"%{term}%")

        # Extract papers from DB
        papers = db.session.query(Paper).filter(termFilter)

        if not isGlobal:
            papers = papers.filter(
            (Paper.year >= 2020) | (Paper.citedcount == 0) | ((Paper.citedcount >= 30) & (Paper.citedcount < 36))).all()

        # Filter keywords
        matched_keywords = []
        for paper in papers:
            if paper.keywords_ru:
                keywords = [kw.strip().lower()
                            for kw in paper.keywords_ru.split(',')]
                for keyword in keywords:
                    if keyword not in matched_keywords:
                        for term in termsRu:
                            if term in keyword:
                                matched_keywords.append(keyword)
                                break

            if paper.keywords_en:
                keywords = [kw.strip().lower()
                            for kw in paper.keywords_en.split(',')]
                for keyword in keywords:
                    if keyword not in matched_keywords:
                        for term in termsEn:
                            if term in keyword:
                                matched_keywords.append(keyword)
                                break

        # Sort keywords
        matched_keywords.sort()

        return {
            'papers': [i.serialize for i in papers],
            'terms': termsRu + termsEn,
            'keywords': matched_keywords
        }

    """Search in Scopus"""
    @staticmethod
    def search_scopus(termsEn):
        # Create filter
        # NOTE: abs(image crystal) - in any order, abs({image crystal}) - exact string
        terms = ' '.join(termsEn)
        query = f'ABS({terms}) or TITLE({terms}) or KEY({terms})'
        # NOTE: do not use >= or <=, spaces around sign are mandatory
        query = f'({query}) and ((YEAR > 2017) or (PUBYEAR > 2017))'

        papers = []

        data = Scopus.searchRequest(query, popularFirst=True)
        if 'search-results' in data:
            total = int(data['search-results']['opensearch:totalResults'])
            start = int(data['search-results']['opensearch:startIndex'])
            page = int(data['search-results']['opensearch:itemsPerPage'])
            for i in range(page):
                entry = data['search-results']['entry'][i]
                paper = {
                    'id': entry.get('eid', i),
                    'title_en': entry.get('dc:title'),
                    'creator_en': entry.get('dc:creator'),
                    'source': entry.get('prism:publicationName'),
                    'year': entry.get('prism:coverDisplayDate'),
                    'volume': entry.get('prism:volume'),
                    'issue': entry.get('prism:issueIdentifier'),
                    'pages': entry.get('prism:pageRange'),
                    'doi': entry.get('prism:doi'),
                    'citedcount': entry.get('citedby-count', 0),
                }

                date = entry.get('prism:coverDate', '')
                paper['date'] = date
                year = re.search(r'\d\d\d\d', date)
                if year:
                    paper['year'] = year[0]

                links = entry.get('link', [])
                for j in range(len(links)):
                    link = links[j]
                    ref = link.get('@ref')
                    if ref == 'scopus':
                        paper['link'] = link.get('@href')
                        break

                papers.append(paper)

        return {
            'papers': papers,
            'terms': termsEn
        }

    """Provide pdf proxy"""
    @staticmethod
    def pdf_co(id):
        paper = db.session.query(Paper).filter(Paper.id == id).first()

        if not paper or not paper.pdf:
            return 'Not found', 404

        req = requests.get(paper.pdf, stream=True)

        filename = os.path.basename(paper.pdf)

        headers = {
            'Content-Type': req.headers["content-type"],
            'Content-Disposition':
            f'attachment; filename={filename}'
        }

        return Response(stream_with_context(req.iter_content(chunk_size=2048)), headers=headers)
