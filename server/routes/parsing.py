from flask import Blueprint
from app.controllers.parser import Parser
from app.controllers.filler import Filler
from app.controllers.scopus import Scopus
from .api import api


@api.route('/parse', methods=['GET'])
def parse():
    return Parser.parse()


@api.route('/fill-data-ru', methods=['GET'])
def fillDataRu():
    return Filler.fill_data_ru()


@api.route('/fill-base-en', methods=['GET'])
def fillBaseEn():
    return Filler.fill_base_en()


@api.route('/fill-data-en', methods=['GET'])
def fillDataEn():
    return Filler.fill_data_en()


@api.route('/fill-years', methods=['GET'])
def fillYears():
    return Filler.fill_years()


@api.route('/scopus-link', methods=['GET'])
def scopusLink():
    return Scopus.link()


@api.route('/scopus-fix', methods=['GET'])
def scopusFix():
    return Scopus.fix()
