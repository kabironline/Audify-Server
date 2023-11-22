from music.models import Album, AlbumItem, Track
from membership.services import get_user_by_username, get_user_by_id, get_user_dict
from core.db import get_session
from core import get_current_user
from werkzeug.datastructures import FileStorage
import os.path
from datetime import datetime


def create_album(
    name,
    description="",
    release_date: datetime = datetime.now(),
    album_art: FileStorage = None,
    channel_id=0,
    api=False,
):
    session = get_session()

    user = None
    if api:
        user = get_user_by_username("api_superuser")
    else:
        user = get_current_user()

    album = Album(
        name=name,
        description=description,
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        release_date=release_date,
        created_by=channel_id,
        last_modified_by=channel_id,
    )

    session.add(album)
    session.commit()

    album = session.query(Album).filter_by(name=name).first()

    if album_art is not None:
        try:
            os.mkdir(f"media/albums/{album.id}")
            album_art.save(f"media/albums/{album.id}/album_art.png")
        except Exception as e:
            session.rollback()
            os.rmdir(f"media/albums/{album.id}")

    session.close()

    return album


def get_album_by_id(album_id):
    session = get_session()

    album = session.query(Album).filter_by(id=album_id).first()

    session.close()

    return album


def get_album_by_name(album_name):
    pass


def get_album_by_user(user_id):
    session = get_session()

    album = session.query(Album).filter_by(created_by=user_id).all()

    session.close()

    return album


def get_latest_albums(limit=5):
    session = get_session()

    albums = session.query(Album).order_by(Album.created_at.desc()).limit(limit).all()

    session.close()

    return albums


def update_album(
    album_id,
    name="",
    description="",
    release_date: datetime = None,
    album_art: FileStorage = None,
):
    session = get_session()

    album = session.query(Album).filter_by(id=album_id).first()

    album.name = name if name != "" and name is not None else album.name
    album.description = (
        description if description != "" and description is None else album.description
    )
    album.release_date = (
        release_date if release_date is not None else album.release_date
    )
    album.last_modified_at = datetime.now()
    album.last_modified_by = album.created_by

    session.commit()

    if album_art is not None:
        if album_art.filename == "":
            session.close()
            return album
        try:
            os.mkdir(f"media/albums/{album_id}")
        except FileExistsError:
            pass
        album_art.save(f"media/albums/{album_id}/album_art.png")

    session.close()
    return album


def delete_album(album_id, channel_id=0, api=False):
    session = get_session()

    # Check if the album belongs to the user
    album = get_album_by_id(album_id)
    if album is None or album.created_by != channel_id:
        return None

    if channel_id == 0 and not api:
        return None

    album_tracks = get_album_items_by_album_id(album_id)
    for album_track in album_tracks:
        delete_album_item(album_track.id)
    try:
        files = os.listdir(f"media/albums/{album_id}")
        for file in files:
            os.remove(f"media/albums/{album_id}/{file}")
        os.rmdir(f"media/albums/{album_id}")
    except FileNotFoundError:
        pass

    session.delete(album)
    session.commit()
    session.close()

    return album


def get_album_dict(album):
    user = get_user_dict(get_user_by_id(album.created_by))

    album_dict = {
        "id": album.id,
        "name": album.name,
        "description": album.description,
        "created_at": album.created_at,
        "last_modified_at": album.last_modified_at,
        "created_by": user,
        "last_modified_by": album.last_modified_by,
    }

    return album_dict


# -----------------------------Album Items-----------------------------------


def create_album_item(album_id, track_id, user_id=0, api=False):
    session = get_session()

    album = session.query(Album).filter_by(id=album_id).first()
    if album is None or album.created_by != user_id:
        return None

    track = session.query(Track).filter_by(id=track_id).first()
    if track is None:
        return None

    if user_id == 0 and not api:
        return None

    if (
        session.query(AlbumItem).filter_by(album_id=album_id, track_id=track_id).first()
        is not None
    ):
        return None

    album_item = AlbumItem(
        album_id=album_id,
        track_id=track_id,
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        created_by=user_id,
        last_modified_by=user_id,
    )

    session.add(album_item)
    session.commit()
    session.close()

    return album_item


def get_album_items_by_album_id(album_id):
    session = get_session()

    album_items = session.query(AlbumItem).filter_by(album_id=album_id).all()

    session.close()

    return album_items


def get_track_albums(track_id):
    session = get_session()

    album_items = session.query(AlbumItem).filter_by(track_id=track_id).all()

    session.close()

    return album_items


def delete_album_item(album_item_id):
    session = get_session()

    album_item = session.query(AlbumItem).filter_by(id=album_item_id).first()

    session.delete(album_item)
    session.commit()
    session.close()

    return album_item


def delete_album_item_by_album_track_id(album_id, track_id):
    session = get_session()

    album_item = (
        session.query(AlbumItem).filter_by(album_id=album_id, track_id=track_id).first()
    )

    session.delete(album_item)
    session.commit()
    session.close()

    return album_item
