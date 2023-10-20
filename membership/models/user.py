from sqlalchemy import ForeignKey
from datetime import datetime as DateTime
from sqlalchemy.orm import mapped_column, Mapped
from core.db import Base


class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True)
    nickname: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_by: Mapped[int] = mapped_column(  # Change "id" to "int"
        ForeignKey('User.id'), nullable=True)
    last_modified_by: Mapped[int] = mapped_column(  # Change "User.id" to "int"
        ForeignKey('User.id'), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(nullable=False)
    last_modified_at: Mapped[DateTime] = mapped_column(nullable=False)

    def __init__(self, username, password, created_by=None, last_modified_by=None, nickname="", bio="", is_admin=False):
        self.username = username
        self.nickname = nickname if nickname == "" else username
        self.bio = bio
        self.password = password
        self.is_admin = is_admin
        self.created_by = created_by
        self.last_modified_by = last_modified_by
        self.created_at = DateTime.utcnow()
        self.last_modified_at = DateTime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username
