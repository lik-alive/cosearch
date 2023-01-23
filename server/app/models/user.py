from app.db import db

"""User model."""


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
