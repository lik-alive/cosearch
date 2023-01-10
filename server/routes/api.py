from flask import Blueprint
from app.controllers.parser import Parser
from app.controllers.filler import Filler

api = Blueprint("api", __name__, url_prefix="/api")

@api.route('/parse')
def parse():
    return Parser.parse()

@api.route('/fill-data-ru')
def fillDataRu():
    return Filler.fill_data_ru()

@api.route('/fill-base-en')
def fillBaseEn():
    return Filler.fill_base_en()

@api.route('/fill-data-en')
def fillDataEn():
    return Filler.fill_data_en()
