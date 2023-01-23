from app.controllers.searcher import Searcher
from .api import api
from flask_jwt_extended import jwt_required


@api.route('/search-co', methods=['POST'])
@jwt_required()
def searchCO():
    return Searcher.search('co')


@api.route('/pdf-co/<id>', methods=['GET'])
def pdfCO(id):
    return Searcher.pdf_co(id)


@api.route('/search-scopus', methods=['POST'])
@jwt_required()
def searchScopus():
    return Searcher.search('scopus')
