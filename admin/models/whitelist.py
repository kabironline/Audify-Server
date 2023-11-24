from sqlalchemy import ForeignKey
from core.db import db


class Whitelist(db.Model):
    __tablename__ = "Whitelist"
    channel_id = db.Column(db.Integer, ForeignKey("Channel.id"), primary_key=True)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
