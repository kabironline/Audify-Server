from sqlalchemy import ForeignKey
from core.db import db


class Recent(db.Model):
    __tablename__ = "Recent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    track_id = db.Column(db.Integer, ForeignKey("Track.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
