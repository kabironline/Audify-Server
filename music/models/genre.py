from core.db import db


class Genre(db.Model):
    __tablename__ = "Genre"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True, index=True)
    color = db.Column(db.String(6), nullable=False)
