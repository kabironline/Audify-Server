from sqlalchemy import ForeignKey
from core.db import db


class Channel(db.Model):
    __tablename__ = "Channel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.String(200), nullable=True)
    blacklisted = db.Column(db.Boolean, nullable=True)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)


class ChannelSearch(db.Model):
    __tablename__ = "ChannelSearch"
    rowid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
