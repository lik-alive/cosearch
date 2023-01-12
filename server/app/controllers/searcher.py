import os
import re
import requests
from flask import jsonify, request, Response, stream_with_context
from app.actions.translator import Translator
from app.db import db
from app.models.paper import Paper
from sqlalchemy.sql import false


class Searcher:
    """Search for papers."""

    @staticmethod
    def search_co():
        data = request.get_json() or {}

        # No term provided
        if not 'query' in data:
            return "Query is required", 422

        query = data['query']

        # Too long query
        if len(query) > 255:
            return "Query should not exceed 255 characters", 422

        # Split terms and convert to lower case
        terms = [t.strip().lower()
                 for t in query.split(',') if len(t.strip()) > 3]

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

        # Create filter
        termFilter = false()
        for term in termsRu:
            termFilter |= Paper.title_ru.like(f"%{term}%") | Paper.keywords_ru.like(
                f"%{term}%") | Paper.abstract_ru.like(f"%{term}%")
        for term in termsEn:
            termFilter |= Paper.title_en.like(f"%{term}%") | Paper.keywords_en.like(
                f"%{term}%") | Paper.abstract_en.like(f"%{term}%")

        # Extract papers from DB
        papers = db.session.query(Paper).filter(termFilter).all()

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

        db.session.close()

        return jsonify({
            'papers': [i.serialize for i in papers],
            'terms': termsRu + termsEn,
            'keywords': matched_keywords
        })

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
