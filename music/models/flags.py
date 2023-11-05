from sqlalchemy import ForeignKey
from core.db import db

class Flag(db.Model):
    __tablename__ = "Flag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reason = db.Column(db.String(50), nullable=False, unique=True, index=True)
    flaged_by = db.Column(db.Integer, ForeignKey('User.id'), nullable=True)
    flaged_at = db.Column(db.DateTime, nullable=False)
