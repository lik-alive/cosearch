from flask import Blueprint
import logging
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError

api = Blueprint("api", __name__, url_prefix="/api")

# Global error handler
@api.errorhandler(Exception)
def handle_error(e):
    # Skip expired signature error
    if isinstance(e, ExpiredSignatureError):
        return "Unauthorized", 401

    # Skip no authorization error
    if isinstance(e, NoAuthorizationError):
        return "Unauthorized", 401

    logging.error(e)    
    return "Server error", 500
