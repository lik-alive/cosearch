from app.db import db
from app.controllers.parserComps.info import Info


class Paper(db.Model):
    """Paper model."""

    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer)
    title_ru = db.Column(db.String(1024))
    authors_ru = db.Column(db.String(1024))
    keywords_ru = db.Column(db.String(1024))
    citation_ru = db.Column(db.String(1024))
    abstract_ru = db.Column(db.Text)
    title_en = db.Column(db.String(1024))
    authors_en = db.Column(db.String(1024))
    keywords_en = db.Column(db.String(1024))
    citation_en = db.Column(db.String(1024))
    abstract_en = db.Column(db.Text)
    issue = db.Column(db.String(8))
    year = db.Column(db.Integer)
    pdf = db.Column(db.String(255))
    page_ru = db.Column(db.String(255))
    page_en = db.Column(db.String(255))
    doi = db.Column(db.String(64))
    eid = db.Column(db.String(64))
    citedcount = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title_ru': self.title_ru,
            'authors_ru': self.authors_ru,
            'keywords_ru': self.keywords_ru,
            'abstract_ru': self.abstract_ru,
            'citation_ru': self.citation_ru,
            'title_en': self.title_en,
            'authors_en': self.authors_en,
            'keywords_en': self.keywords_en,
            'abstract_en': self.abstract_en,
            'citation_en': self.citation_en,
            'citedcount': self.citedcount,
            'year': self.year,
            'pdf': self.pdf,
            'page_ru': self.page_ru,
            'page_en': self.page_en
        }
