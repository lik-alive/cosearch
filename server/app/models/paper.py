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
    pdf = db.Column(db.String(255))
    page_ru = db.Column(db.String(255))
    page_en = db.Column(db.String(255))
    doi = db.Column(db.String(64))

