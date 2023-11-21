from sqlalchemy import ForeignKey
from core.db import db


class Playlist(db.Model):
    __tablename__ = "Playlist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)


class PlaylistItem(db.Model):
    __tablename__ = "PlaylistItem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, ForeignKey("Playlist.id"), nullable=False)
    track_id = db.Column(db.Integer, ForeignKey("Track.id"), nullable=False)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)


class PlaylistSearch(db.Model):
    __tablename__ = "PlaylistSearch"
    rowid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
