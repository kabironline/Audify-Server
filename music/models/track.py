from sqlalchemy import ForeignKey
from core.db import db


class Track(db.Model):
    __tablename__ = "Track"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.String, nullable=True)
    release_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=True, default=0)
    flag_id = db.Column(db.Integer, ForeignKey("Flag.id"), nullable=True)
    flagged = db.Column(db.Boolean, nullable=True)
    genre_id = db.Column(db.Integer, ForeignKey("Genre.id"), nullable=True)
    channel_id = db.Column(db.Integer, ForeignKey("Channel.id"), nullable=True)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)


class TrackSearch(db.Model):
    __tablename__ = "TrackSearch"
    rowid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
