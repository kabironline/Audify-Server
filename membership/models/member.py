from sqlalchemy import ForeignKey
from datetime import datetime as DateTime
from sqlalchemy.orm import mapped_column, Mapped
from .channel import Channel
from .user import User
from core.db import Base


class Member(Base):
    __tablename__ = 'Member'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    channel_id: Mapped["Channel.id"] = mapped_column(
        ForeignKey('Channel.id'),
        nullable=False
    )
    user_id: Mapped["User.id"] = mapped_column(
        ForeignKey('User.id'),
        nullable=False
    )
    created_by: Mapped["User.id"] = mapped_column(
        ForeignKey('User.id'),
        nullable=False
    )
    last_modified_by: Mapped["User.id"] = mapped_column(
        ForeignKey('User.id'),
        nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(nullable=False)
    last_modified_at: Mapped[DateTime] = mapped_column(nullable=True)
