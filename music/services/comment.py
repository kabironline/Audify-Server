from music.models import Comment
from membership.models import User
from core.db import get_session
from datetime import datetime
from sqlalchemy.orm import joinedload


def create_comment(comment, track_id, user_id):
    session = get_session()

    # TODO: Check for SQL injection

    new_comment = Comment(
        comment=comment,
        track_id=track_id,
        user_id=user_id,
        created_by=user_id,
        last_modified_by=user_id,
        last_modified_at=datetime.now(),
        created_at=datetime.now(),
    )

    session = get_session()
    session.add(new_comment)
    session.commit()

    return new_comment


def get_comments_by_track_id(track_id):
    session = get_session()

    comments = (
        session.query(Comment)
        .join(User, Comment.user_id == User.id)
        .options(joinedload(Comment.user))
        .filter(Comment.track_id == track_id)
        .all()
    )

    return comments


def get_comment_by_id(comment_id):
    session = get_session()

    comment = session.query(Comment).filter(Comment.id == comment_id).first()

    return comment


def update_comment(comment_id, comment, user_id):
    session = get_session()

    comment = session.query(Comment).filter(Comment.id == comment_id).first()

    comment.comment = comment
    comment.last_modified_by = user_id
    comment.last_modified_at = datetime.now()

    session.commit()

    return comment


def delete_comment(comment_id):
    session = get_session()

    comment = session.query(Comment).filter(Comment.id == comment_id).first()

    session.delete(comment)
    session.commit()

    return True


def delete_all_comments_by_track_id(track_id):
    session = get_session()

    comments = session.query(Comment).filter(Comment.track_id == track_id).all()

    for comment in comments:
        session.delete(comment)

    session.commit()

    return True


def get_comment_dict(comment: Comment) -> dict:
    return {
        "id": comment.id,
        "comment": comment.comment,
        "track_id": comment.track_id,
        "user_id": comment.user_id,
        "created_at": comment.created_at,
        "created_by": comment.created_by,
        "last_modified_at": comment.last_modified_at,
        "last_modified_by": comment.last_modified_by,
        "user": {
            "id": comment.user.id,
            "username": comment.user.username,
            "nickname": comment.user.nickname,
            "created_at": comment.user.created_at,
            "last_modified_at": comment.user.last_modified_at,
            "created_by": comment.user.created_by,
            "last_modified_by": comment.user.last_modified_by,
        },
    }
