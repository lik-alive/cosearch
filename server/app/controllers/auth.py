from app.db import db
from app.models.user import User
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

"""Auth controller."""


class Auth:

    """Logging user in"""

    @staticmethod
    def login():
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username or not password:
            return jsonify({'msg': 'Credentials required'}), 422

        user = db.session.query(User).filter_by(username=username).first()

        if not user:
            return jsonify({'msg': 'Wrong credentials'}), 400

        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)

            response = jsonify({"msg": "Login successful"})
            set_access_cookies(response, access_token)
            return response

        return jsonify({'msg': 'Wrong credentials'}), 400

    """Registering user"""

    @staticmethod
    def register():
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username or not password:
            return jsonify({'msg': 'Credentials required'}), 422

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()

            return jsonify({'msg': 'Success'}), 201
        else:
            return jsonify({'msg': 'User already exists'}), 202

    """Logging user out"""

    @staticmethod
    def logout():
        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)
        return response
