from app.db import db
from app.controllers.parserComps.info import Info

"""Setting model."""


class Setting(db.Model):

    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(16))
    value = db.Column(db.String(255))
