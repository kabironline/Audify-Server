from sqlalchemy import ForeignKey
from core.db import db


class Member(db.Model):
    __tablename__ = "Member"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    channel_id = db.Column(db.Integer, ForeignKey("Channel.id"), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)
