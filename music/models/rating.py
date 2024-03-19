from sqlalchemy import ForeignKey
from core.db import db


class Rating(db.Model):
    __tablename__ = "Rating"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    track_id = db.Column(db.Integer, ForeignKey("Track.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
