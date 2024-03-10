from music.models import Album, AlbumItem, Track, AlbumSearch
from membership.models import Channel
from membership.services import  get_user_dict, get_channel_by_id, get_channel_dict
from core.db import get_session
from werkzeug.datastructures import FileStorage
import os.path
from datetime import datetime
from sqlalchemy.orm import joinedload


def create_album(
    name,
    description="",
    release_date: datetime = datetime.now(),
    album_art: FileStorage = None,
    channel_id=0,
    api=False,
):
    session = get_session()

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

    album = session.query(Album).filter_by(name=name).filter_by(created_by=channel_id).order_by(Album.created_at.desc()).first()

    if album_art is not None:
        try:
            os.mkdir(f"../media/albums/{album.id}")
            album_art.save(f"../media/albums/{album.id}/album_art.png")
        except Exception as e:
            session.rollback()
            os.rmdir(f"../media/albums/{album.id}")

    session.close()

    return album


def get_album_by_id(album_id):
    session = get_session()

    album = (
        session.query(Album)
        .join(Channel, Album.created_by == Channel.id)
        .options(joinedload(Album.channel))
        .filter(Album.id == album_id)
        .first()
    )

    session.close()

    return album


def get_album_by_name(album_name):
    album = search_albums(album_name)
    if len(album) == 0:
        return None

    return get_album_by_id(album[0].rowid)


def get_album_by_user(channel_id, count=5):
    session = get_session()

    album = (
        session.query(Album)
        .join(Channel, Album.created_by == Channel.id)
        .options(joinedload(Album.channel))
        .filter(Album.created_by == channel_id)
        .filter(Channel.blacklisted.is_(None), Channel.is_active.is_(None))
        .order_by(Album.created_at.desc())
        .limit(count)
        .all()
    )

    session.close()

    return album


def get_latest_albums(limit=5):
    session = get_session()

    albums = (
        session.query(Album)
        .join(Channel, Album.created_by == Channel.id)
        .options(joinedload(Album.channel))
        .order_by(Album.created_at.desc())
        .filter(Channel.blacklisted.is_(None), Channel.is_active.is_(None))
        .limit(limit)
        .all()
    )

    session.close()

    return albums


def get_all_albums():
    session = get_session()

    albums = (
        session.query(Album, Channel.name.label("channel_name"))
        .join(Channel, Channel.id == Album.created_by)
        .options(joinedload(Album.channel))
        .filter(Channel.blacklisted.is_(None), Channel.is_active.is_(None))
        .all()
    )

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
            os.mkdir(f"../media/albums/{album_id}")
        except FileExistsError:
            pass
        album_art.save(f"../media/albums/{album_id}/album_art.png")

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
        files = os.listdir(f"../media/albums/{album_id}")
        for file in files:
            os.remove(f"../media/albums/{album_id}/{file}")
        os.rmdir(f"../media/albums/{album_id}")
    except FileNotFoundError:
        pass

    session.delete(album)
    session.commit()
    session.close()

    return album


def get_album_dict(album):
    user = get_channel_dict(get_channel_by_id(album.created_by))

    toString = lambda x: x.strftime("%Y-%m-%d %H:%M:%S")

    album_dict = {
        "id": album.id,
        "name": album.name,
        "description": album.description,
        "created_at": toString(album.created_at),
        "last_modified_at": toString(album.last_modified_at),
        "last_modified_by": album.last_modified_by,
        "created_by": user,
    }

    return album_dict


def search_albums(search_term):
    return AlbumSearch.query.filter(AlbumSearch.name.match(search_term)).all()


# -----------------------------Album Items-----------------------------------


def create_album_item(album_id, track_id, user_id=0, api=False):
    session = get_session()

    album = session.query(Album).filter_by(id=album_id).first()
    if album is None or album.created_by != user_id:
        return None

    track = session.query(Track).filter_by(id=track_id).first()
    if track is None:
        return None

    import pdb; pdb.set_trace()

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


def get_album_tracks_by_album_id(album_id):
    session = get_session()

    album_items = (
        session.query(Track)
        .join(AlbumItem, Track.id == AlbumItem.track_id)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .filter(
            Track.flagged.is_(None),
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
        )
        .filter(AlbumItem.album_id == album_id)
        .all()
    )

    session.close()

    return album_items


def get_album_items_by_album_id(album_id):
    session = get_session()

    album_items = session.query(AlbumItem).filter_by(album_id=album_id).all()

    session.close()

    return album_items


def get_track_albums(track_id):
    session = get_session()

    album_items = (
        session.query(Track)
        .join(AlbumItem, Track.id == AlbumItem.track_id)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .filter(
            Track.flagged.is_(None),
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
        )
        .filter(AlbumItem.track_id == track_id)
        .all()
    )

    session.close()

    return album_items


def get_item_albums(track_id):
    session = get_session()

    album_items = session.query(AlbumItem).filter(AlbumItem.track_id == track_id).all()

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
