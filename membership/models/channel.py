from sqlalchemy import ForeignKey
from datetime import datetime as DateTime
from sqlalchemy.orm import mapped_column, Mapped
from .user import User
from core.db import Base


class Channel(Base):
    __tablename__ = 'Channel'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    created_by: Mapped["User.id"] = mapped_column(
        ForeignKey('User.id'), nullable=True)
    last_modified_by: Mapped["User.id"] = mapped_column(
        ForeignKey('User.id'), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(nullable=False)
    last_modified_at: Mapped[DateTime] = mapped_column(nullable=True)
