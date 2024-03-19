from sqlalchemy import ForeignKey
from core.db import db


class View(db.Model):
    __tablename__ = "View"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_id = db.Column(db.Integer, ForeignKey("Track.id"))
    genre_id = db.Column(db.Integer, ForeignKey("Genre.id"))
    user_id = db.Column(db.Integer, ForeignKey("User.id"))
    channel_id = db.Column(db.Integer, ForeignKey("Channel.id"))
    created_at = db.Column(db.DateTime)
    last_updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("User.id"))
    last_updated_by = db.Column(db.Integer, ForeignKey("User.id"))
