from flask import Blueprint
import logging

api = Blueprint("api", __name__, url_prefix="/api")

# Global error handler
@api.errorhandler(Exception)
def handle_error(e):
    logging.error(e)
    return "Server error", 500
