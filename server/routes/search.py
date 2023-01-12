from app.controllers.searcher import Searcher
from .api import api


@api.route('/search-co', methods=['POST'])
def searchCO():
    return Searcher.search_co()


@api.route('/pdf-co/<id>', methods=['GET'])
def pdfCO(id):
    return Searcher.pdf_co(id)
