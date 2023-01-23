import os
from datetime import timedelta

"""Application config class."""


class Config:

    """JWT"""
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', "secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=float(os.environ.get('JWT_TIMEOUT', 30)))
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False

    """MySQL"""
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')

    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'

    """Scopus"""
    ELS_KEY = os.environ.get('ELS_KEY')

    """Yandex"""
    YA_OAUTH = os.environ.get('YA_OAUTH')
    YA_FOLDERID = os.environ.get('YA_FOLDERID')
