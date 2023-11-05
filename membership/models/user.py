from sqlalchemy import ForeignKey
from core.db import db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False,
                         unique=True, index=True)
    nickname = db.Column(db.String(50), nullable=False,
                         unique=True, index=True)
    bio = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_by = db.Column(db.Integer, ForeignKey('User.id'), nullable=True)
    last_modified_by = db.Column(
        db.Integer, ForeignKey('User.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)
