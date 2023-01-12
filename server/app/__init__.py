from flask import Flask
from flask_cors import CORS
from config import Config
from routes import api
from app.db import db


def create_flask_app(config_class=Config):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Init config
    app.config.from_object(config_class)

    # Init database
    db.init_app(app)

    # Init routes
    app.register_blueprint(api)

    return app
