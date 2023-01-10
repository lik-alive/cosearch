from flask import Flask
from config import Config
from routes.api import api
from app.db import db

def create_flask_app(config_class=Config):
    app = Flask(__name__)

    # Init config
    app.config.from_object(config_class)
    
    # Init database
    db.init_app(app)

    # Init routes
    app.register_blueprint(api)

    return app
