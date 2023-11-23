from music.models import View
from music.services.track import get_track_by_id
import core.db
from datetime import datetime


def create_new_view(track_id, user_id):
    session = core.db.get_session()

    track = get_track_by_id(track_id)

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
    session = core.db.get_session()
    views = session.query(View).filter(View.track_id == track_id).all()
    return views


def get_views_by_user_id(user_id):
    session = core.db.get_session()
    views = session.query(View).filter(View.user_id == user_id).all()
    return views


def get_views_by_channel_id(channel_id):
    session = core.db.get_session()
    views = session.query(View).filter(View.channel_id == channel_id).all()
    return views


def get_views_by_genre_id(genre_id):
    session = core.db.get_session()
    views = session.query(View).filter(View.genre_id == genre_id).all()
    return views


def get_all_views():
    session = core.db.get_session()
    views = session.query(View).all()
    return views


def delete_view_by_id(view_id):
    session = core.db.get_session()
    view = session.query(View).filter(View.id == view_id).first()
    session.delete(view)
    session.commit()
    session.close()


def delete_views_by_track_id(track_id):
    session = core.db.get_session()
    views = session.query(View).filter(View.track_id == track_id).all()
    for view in views:
        session.delete(view)
    session.commit()
    session.close()


def delete_views_by_user_id(user_id):
    session = core.db.get_session()
    views = session.query(View).filter(View.user_id == user_id).all()
    for view in views:
        session.delete(view)
    session.commit()
    session.close()
