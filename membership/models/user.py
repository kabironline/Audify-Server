from sqlalchemy import ForeignKey
from core.db import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True) # Email
    nickname = db.Column(db.String(50), nullable=False, index=True)
    bio = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    last_modified_by = db.Column(db.Integer, ForeignKey("User.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=True, index=True)


    def to_dict(self):
        """
        Returns the dictionary representation of the object.
        """
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "bio": self.bio,
            "is_admin": self.is_admin,
            "created_by": self.created_by,
            "last_modified_by": self.last_modified_by,
            "created_at": self.created_at,
            "last_modified_at": self.last_modified_at,
            "is_active": self.is_active,
        }
