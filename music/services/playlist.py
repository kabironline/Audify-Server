from music.models import Playlist, PlaylistItem, Track, PlaylistSearch, Rating
from membership.models import User, Channel
from membership.services import get_user_by_username, get_user_by_id, get_user_dict
from core.db import get_session
from core import get_current_user
from datetime import datetime
from sqlalchemy.orm import joinedload


def create_playlist(name, description="", api=False, user_id=0):
    session = get_session()

    if not api:
        user_id = get_current_user().id

    playlist = Playlist(
        name=name,
        description=description,
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        created_by=user_id,
        last_modified_by=user_id,
    )

    

    session.add(playlist)
    session.commit()
    playlist_copy = get_playlist_by_id(playlist.id)
    session.close()

    return playlist_copy

def get_playlist_by_id(playlist_id):
    session = get_session()

    playlist = (
        session.query(Playlist)
        .join(User, Playlist.created_by == User.id)
        .options(joinedload(Playlist.user))
        .filter(Playlist.id == playlist_id)
        .first()
    )
    session.close()

    return playlist

def get_latest_user_playlist_by_name(user_id, name,limit=5):
    session = get_session()

    playlist = (
        session.query(Playlist)
        .join(User, Playlist.created_by == User.id)
        .options(joinedload(Playlist.user))
        .filter(Playlist.created_by == user_id)
        .filter(Playlist.name == name)
        .order_by(Playlist.created_at.desc())
        .limit(limit)
        .all()
    )

    return playlist


def get_latest_playlist(limit=5):
    session = get_session()

    playlist = (
        session.query(Playlist)
        .join(User, Playlist.created_by == User.id)
        .options(joinedload(Playlist.user))
        .order_by(Playlist.created_at.desc())
        .limit(limit)
        .all()
    )

    session.close()

    return playlist


def get_playlist_by_user(user_id):
    session = get_session()

    playlist = (
        session.query(Playlist)
        .join(User, Playlist.created_by == User.id)
        .filter(Playlist.created_by == user_id)
        .options(joinedload(Playlist.user))
        .all()
    )

    session.close()

    return playlist


def get_all_playlists():
    session = get_session()

    playlists = (
        session.query(Playlist, User.nickname)
        .join(User, Playlist.created_by == User.id)
        .all()
    )

    session.close()

    return playlists


def update_playlist(playlist_id, name="", description="", user_id = None):
    session = get_session()

    playlist = session.query(Playlist).filter_by(id=playlist_id).first()

    playlist.name = name if name != "" else playlist.name
    playlist.description = description
    playlist.last_modified_at = datetime.now()
    playlist.last_modified_by = user_id if user_id is not None else get_current_user().id

    session.commit()
    session.close()

    return get_playlist_by_id(playlist_id)


def delete_playlist(playlist_id, user_id=0, api=False):
    session = get_session()

    # Check if the playlist belongs to the user
    playlist = get_playlist_by_id(playlist_id)
    if playlist is None or playlist.created_by != user_id:
        return None

    if user_id == 0 and not api:
        return None

    playlist_tracks = get_playlist_items_by_playlist_id(playlist_id)
    for playlist_track in playlist_tracks:
        delete_playlist_item(playlist_track.id)

    session.delete(playlist)
    session.commit()
    session.close()

    return playlist


def get_playlist_dict(playlist):
    user = get_user_dict(get_user_by_id(playlist.created_by))

    toString = lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if x else None

    playlist_dict = {
        "id": playlist.id,
        "name": playlist.name,
        "description": playlist.description,
        "created_at": toString(playlist.created_at),
        "last_modified_at": toString(playlist.last_modified_at),
        "created_by": playlist.created_by,
        "last_modified_by": playlist.last_modified_by,
        "user": user,
    }

    return playlist_dict


def search_playlists(search_term):
    return PlaylistSearch.query.filter(PlaylistSearch.name.match(search_term)).all()


# -----------------------------Playlist Items-----------------------------------


def create_playlist_item(playlist_id, track_id, user_id=0, api=False):
    session = get_session()

    playlist = session.query(Playlist).filter_by(id=playlist_id).first()
    if playlist is None or playlist.created_by != user_id:
        return None

    track = session.query(Track).filter_by(id=track_id).first()
    if track is None:
        return None

    if user_id == 0 and not api:
        return None

    if (
        session.query(PlaylistItem)
        .filter_by(playlist_id=playlist_id, track_id=track_id)
        .first()
        is not None
    ):
        return None

    playlist_item = PlaylistItem(
        playlist_id=playlist_id,
        track_id=track_id,
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        created_by=user_id,
        last_modified_by=user_id,
    )

    session.add(playlist_item)
    session.commit()
    session.close()

    return playlist_item


def get_tracks_by_playlist_id(playlist_id):
    session = get_session()
    user = get_current_user()

    playlist_items = (
        session.query(Track)
        .join(PlaylistItem, Track.id == PlaylistItem.track_id)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .filter(
            Track.flagged.is_(None),
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
        )
        .filter(PlaylistItem.playlist_id == playlist_id)
        .all()
    )

    session.close()

    return playlist_items


def get_playlist_items_by_playlist_id(playlist_id):
    session = get_session()

    playlist_items = (
        session.query(PlaylistItem)
        .filter(PlaylistItem.playlist_id == playlist_id)
        .all()
    )

    session.close()

    return playlist_items


def get_track_playlists(track_id):
    session = get_session()

    playlist_items = session.query(PlaylistItem).filter_by(track_id=track_id).all()

    session.close()

    return playlist_items


def delete_playlist_item(playlist_item_id):
    session = get_session()

    playlist_item = session.query(PlaylistItem).filter_by(id=playlist_item_id).first()

    session.delete(playlist_item)
    session.commit()
    session.close()

    return playlist_item


def delete_playlist_item_by_playlist_track_id(playlist_id, track_id):
    session = get_session()

    playlist_item = (
        session.query(PlaylistItem)
        .filter_by(playlist_id=playlist_id, track_id=track_id)
        .first()
    )

    session.delete(playlist_item)
    session.commit()
    session.close()

    return playlist_item
