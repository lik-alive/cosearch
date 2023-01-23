from app.controllers.auth import Auth
from .api import api
from flask_jwt_extended import get_jwt, get_jwt_identity, create_access_token, set_access_cookies
from datetime import datetime, timedelta


@api.route('/login', methods=['POST'])
def login():
    return Auth.login()


# @api.route('/register', methods=['POST'])
# def register():
#     return Auth.register()


@api.route('/logout', methods=['GET'])
def logout():
    return Auth.logout()


"""Refresh JWT token"""


@api.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        target_timestamp = datetime.timestamp(
            datetime.utcnow() + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
