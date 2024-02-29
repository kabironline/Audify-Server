from music.models import Recent, Track
from membership.models import Channel
from core.db import get_session, db
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import desc


def create_recent(user_id, track_id):
    session = get_session()

    # Checking if the track is already in the recent table for the user
    recent = get_recent_by_user_and_track_id(user_id, track_id)
    if recent is not None:
        delete_recent_by_user_and_track_id(user_id, track_id)

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
        session.query(Track)
        .join(Recent, Track.id == Recent.track_id)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .filter(
            Recent.user_id == user_id,
            Recent.track_id == track_id,
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
            Track.flagged.is_(None),
        )
        .first()
    )


def get_recent_by_user_id(user_id, count=10):
    session = get_session()
    # sort them in descending order by last_modified_at
    query = (
        session.query(Track)
        .join(Recent, Track.id == Recent.track_id)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .order_by(desc(Recent.last_modified_at))
        .filter(
            Recent.user_id == user_id,
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
            Track.flagged.is_(None),
        )
        .limit(count)
        .all()
    )

    return query


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


def delete_recent_by_user_and_track_id(user_id, track_id):
    session = get_session()
    session.query(Recent).filter(
        Recent.user_id == user_id, Recent.track_id == track_id
    ).delete()
    session.commit()
    return True
