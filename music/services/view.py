from music.models import View, Track
from membership.models import Channel
from music.services.track import get_track_by_id
from core.db import get_session, db
from datetime import datetime
from sqlalchemy.orm import joinedload


def create_new_view(track, user_id):
    session = get_session()

    view = View(
        track_id=track.id,
        genre_id=track.genre_id,
        user_id=user_id,
        channel_id=track.channel_id,
        created_by=user_id,
        last_updated_by=user_id,
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )

    session.add(view)
    session.commit()


def get_views_by_track_id(track_id):
    session = get_session()
    # return the count of views
    views = session.query(View.id).filter(View.track_id == track_id).count()
    return views


def get_views_by_user_id(user_id):
    session = get_session()
    views = session.query(View.id).filter(View.user_id == user_id).count()
    return views


def get_views_by_channel_id(channel_id):
    session = get_session()
    views = session.query(View.id).filter(View.channel_id == channel_id).count()
    return views


def get_views_by_genre_id(genre_id):
    session = get_session()
    views = session.query(View.id).filter(View.genre_id == genre_id).count()
    return views


def get_all_views():
    session = get_session()
    views = session.query(View).all()
    return views


def get_top_tracks(count=5):
    session = get_session()

    query = (
        session.query(Track)
        .join(View, Track.id == View.track_id)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .group_by(Track.id)
        .filter(Channel.blacklisted.is_(None), Track.flagged.is_(None))
        .order_by(db.func.count(View.id).desc())
        .limit(count)
        .all()
    )
    return query


def delete_view_by_id(view_id):
    session = get_session()
    view = session.query(View).filter(View.id == view_id).first()
    session.delete(view)
    session.commit()
    session.close()


def delete_views_by_track_id(track_id):
    session = get_session()
    views = session.query(View).filter(View.track_id == track_id).all()
    for view in views:
        session.delete(view)
    session.commit()
    session.close()


def delete_views_by_user_id(user_id):
    session = get_session()
    views = session.query(View).filter(View.user_id == user_id).all()
    for view in views:
        session.delete(view)
    session.commit()
    session.close()
