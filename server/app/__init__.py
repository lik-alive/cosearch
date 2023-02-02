from flask import Flask
from flask_cors import CORS
from config import Config
from routes import api
from app.db import db
from flask_jwt_extended import JWTManager
from app.log import log


def create_flask_app(config_class=Config):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True)

    # Init config
    app.config.from_object(config_class)

    # Init logging
    log.init()

    # Init database
    db.init_app(app)

    # Init JWT
    JWTManager(app)

    # Init routes
    app.register_blueprint(api)

    return app
