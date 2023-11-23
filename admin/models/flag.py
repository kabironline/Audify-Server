from sqlalchemy import ForeignKey
from core.db import db


class TrackFlag(db.Model):
    __tablename__ = "TrackFlag"
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, ForeignKey("Track.id"))
    reported_by = db.Column(db.Integer, ForeignKey("User.id"))
    approved_by = db.Column(db.Integer, ForeignKey("User.id"))
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    last_updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("User.id"))
    last_updated_by = db.Column(db.Integer, ForeignKey("User.id"))


class UserFlag(db.Model):
    __tablename__ = "UserFlag"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("User.id"))
    reported_by = db.Column(db.Integer, ForeignKey("User.id"))
    approved_by = db.Column(db.Integer, ForeignKey("User.id"))
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    last_updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("User.id"))
    last_updated_by = db.Column(db.Integer, ForeignKey("User.id"))


class ChannelFlag(db.Model):
    __tablename__ = "ChannelFlag"
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, ForeignKey("Channel.id"))
    reported_by = db.Column(db.Integer, ForeignKey("User.id"))
    approved_by = db.Column(db.Integer, ForeignKey("User.id"))
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    last_updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("User.id"))
    last_updated_by = db.Column(db.Integer, ForeignKey("User.id"))
