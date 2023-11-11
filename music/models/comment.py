from sqlalchemy import ForeignKey
from core.db import db


class Comment(db.Model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(500), nullable=False)
    track_id = db.Column(db.Integer, ForeignKey("Track.id"), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
