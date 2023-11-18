from music.models import Recent
from core.db import get_session
from datetime import datetime


def create_recent(user_id, track_id):
    session = get_session()

    # Checking if the track is already in the recent table for the user
    recent = get_recent_by_user_and_track_id(user_id, track_id)
    if recent is not None:
        recent.last_modified_at = datetime.now()
        recent.last_modified_by = user_id
        session.commit()
        return recent

    recent = Recent(
        user_id=user_id,
        track_id=track_id,
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        created_by=user_id,
        last_modified_by=user_id,
    )
    session.add(recent)
    session.commit()
    return recent


def get_recent_by_user_and_track_id(user_id, track_id):
    session = get_session()
    return (
        session.query(Recent)
        .filter(Recent.user_id == user_id, Recent.track_id == track_id)
        .first()
    )


def get_recent_by_user_id(user_id):
    session = get_session()
    # sort them in descending order by last_modified_at
    return (
        session.query(Recent)
        .filter(Recent.user_id == user_id)
        .order_by(Recent.last_modified_at.desc())
        .limit(10)
        .all()
    )


def delete_recent_by_user_id(user_id):
    session = get_session()
    session.query(Recent).filter(Recent.user_id == user_id).delete()
    session.commit()
    return True


def delete_recent_by_track_id(track_id):
    session = get_session()
    session.query(Recent).filter(Recent.track_id == track_id).delete()
    session.commit()
    return True
