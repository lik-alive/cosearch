from app.db import db


class User(db.Model):
    """User model."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32))
    password = db.Column(db.String(32))
