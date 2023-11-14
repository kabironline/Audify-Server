from music.models import Comment
from core.db import get_session
from datetime import datetime


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

    comments = session.query(Comment).filter(Comment.track_id == track_id).all()

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