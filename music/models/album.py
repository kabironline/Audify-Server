from sqlalchemy import ForeignKey
from core.db import db


class Album(db.Model):
    __tablename__ = "Album"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)


class AlbumItem(db.Model):
    __tablename__ = "AlbumItem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_id = db.Column(db.Integer, ForeignKey("Album.id"), nullable=False)
    track_id = db.Column(db.Integer, ForeignKey("Track.id"), nullable=False)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)


class AlbumSearch(db.Model):
    __tablename__ = "AlbumSearch"
    rowid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
