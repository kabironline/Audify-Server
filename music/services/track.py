from membership.models import Channel
from music.models import Track, Rating, TrackSearch, View
from music.services.rating import *
from music.services.playlist import (
    get_track_playlists,
    delete_playlist_item_by_playlist_track_id,
)
from music.services.album import (
    get_item_albums,
    delete_album_item,
)
from music.services.comment import delete_all_comments_by_track_id
from music.services.recent import delete_recent_by_track_id
from music.services.view import delete_views_by_track_id
from core.db import get_session, get_db
from datetime import datetime
from werkzeug.datastructures import FileStorage
import os
import mutagen.mp3
from sqlalchemy.orm import joinedload

db = get_db()


def create_track(
    name,
    lyrics,
    release_date: datetime,
    media: FileStorage,
    track_art: FileStorage,
    channel_id,
    genre_id=10,
):
    """
    Creates a track with the given name, lyrics, release_date

    It performs the following tasks.

    - Checks if the media is a valid media file.
        - Only mp3 files are allowed.
    - Checks if the media file is not empty.

    In case of any validation failure, it raises an exception.

    The media will be uploaded to a "../media/tracks/{track.id}/audio" folder and the
    media should be renamed into a uuid string.

    The database will store the uuid string of the media file.

    The track-art will be uploaded to a "../media/tracks/{track-id}/track-art" folder and the
    track-art should be renamed into a uuid string.

    The database will store the uuid string of the track-art file.
    """

    session = get_session()
    duration = 0
    if media is not None:
        if not media.filename.endswith(".mp3") or media.filename == "":
            raise Exception("Invalid media file")
        duration = int(mutagen.mp3.MP3(media).info.length)

    track = Track(
        name=name,
        lyrics=lyrics,
        release_date=release_date,
        channel_id=channel_id,
        genre_id=genre_id,
        created_by=channel_id,
        duration=int(duration),
        flagged=None,
        last_modified_by=channel_id,
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
    )

    session.add(track)
    session.commit()

    # Get the track id
    track_id = track.id

    try:
        # Create a folder for the track
        os.mkdir(f"../media/tracks/{track_id}")

        media.save(f"../media/tracks/{track_id}/audio.mp3")
        track_art.save(f"../media/tracks/{track_id}/track-art.png")
    except Exception as e:
        session.rollback()
        os.rmdir(f"../media/tracks/{track_id}")
        raise e
    session.close()

    return track_id


def get_track_by_id(track_id, user_id=None, rating=False):
    session = get_session()

    track = (
        session.query(Track)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .filter(Track.id == track_id)
        .first()
    )

    if rating:
        track.rating = get_rating_by_user_and_track_id(user_id, track.id)

    session.close()

    return track


def get_all_tracks(channel=True):
    session = get_session()
    if channel:
        tracks = (
            session.query(Track)
            .options(joinedload(Track.channel))
            .order_by(Track.flagged.is_(True).desc())
            # .order_by(Track.id.asc())
            .join(Channel, Track.channel_id == Channel.id)
            .all()
        )
    else:
        tracks = session.query(Track).all()
    session.close()

    return tracks


def get_tracks_by_channel(channel_id, user_id=None, rating=False, count=5):
    session = get_session()
    tracks = None
    if rating:
        tracks = (
            session.query(Track)
            .join(Channel, Track.channel_id == Channel.id)
            .options(joinedload(Track.channel))
            .filter(
                Track.channel_id == channel_id,
                Track.flagged.is_(None),
                Channel.blacklisted.is_(None),
                Channel.is_active.is_(None),
            )
            .order_by(Track.last_modified_at.desc())
            .limit(count)
            .all()
        )
        for track in tracks:
            track.rating = get_rating_by_user_and_track_id(user_id, track.id)
    else:
        tracks = (
            session.query(Track)
            .join(Channel, Track.channel_id == Channel.id)
            .options(joinedload(Track.channel))
            .filter(
                Track.channel_id == channel_id,
                Track.flagged.is_(None),
                Channel.blacklisted.is_(None),
                Channel.is_active.is_(None),
            )
            .order_by(Track.last_modified_at.desc())
            .limit(count)
            .all()
        )

    session.close()

    return tracks


def get_channel_tracks_by_views(channel_id, count=5):
    session = get_session()

    tracks = (
        session.query(Track)
        .join(Channel, Track.channel_id == Channel.id)
        .join(View, Track.id == View.track_id)
        .options(joinedload(Track.channel))
        .filter(Channel.id == channel_id, Track.flagged.is_(None))
        .group_by(Track.id)
        .order_by(View.count.desc())
        .limit(count)
        .all()
    )

    session.close()

    return tracks


def get_top_rated_tracks(count=5):
    session = get_session()

    query = (
        session.query(Track)
        .join(Rating, Track.id == Rating.track_id)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .filter(
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
            Track.flagged.is_(None),
        )
        .group_by(Track.id)
        .having(db.func.avg(Rating.rating) > 0, db.func.count(Rating.rating) > 0)
        .order_by(db.func.avg(Rating.rating).desc())
        .limit(count)
        .all()
    )

    return query


def get_top_rated_channels(count=5):
    session = get_session()

    db = get_db()

    query = (
        db.session.query(Channel)
        .join(Track, Channel.id == Track.channel_id)
        .join(Rating, Track.id == Rating.track_id)
        .filter(
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
            Track.flagged.is_(None),
        )
        .group_by(Channel.id)
        .having(db.func.avg(Rating.rating) > 0, db.func.count(Rating.rating) > 0)
        .order_by(db.func.avg(Rating.rating).desc())
        .limit(count)
        .all()
    )

    return query


def get_latest_tracks(count=5):
    session = get_session()
    tracks = (
        session.query(Track)
        .join(Channel, Track.channel_id == Channel.id)
        .options(joinedload(Track.channel))
        .filter(
            Channel.blacklisted.is_(None),
            Channel.is_active.is_(None),
            Track.flagged.is_(None),
        )
        .order_by(Track.created_at.desc())
        .limit(count)
        .all()
    )
    session.close()

    return tracks


def update_track(
    track_id,
    name=None,
    lyrics=None,
    genre=None,
    release_date=None,
    duration: int = 0,
    media: FileStorage = None,
    track_art: FileStorage = None,
):
    session = get_session()

    track = session.query(Track).filter(Track.id == track_id).first()

    if track is None:
        return None

    track.name = name if name is not None else track.name
    track.lyrics = lyrics if lyrics is not None else track.lyrics
    track.release_date = (
        release_date if release_date is not None else track.release_date
    )
    track.genre_id = genre if genre is not None else track.genre_id
    track.duration = duration if duration != 0 else track.duration
    try:
        if media.filename != "":
            track.duration = int(mutagen.mp3.MP3(media).info.length)
            media.save(f"../media/tracks/{track_id}/audio.mp3")
        if track_art.filename != "":
            track_art.save(f"../media/tracks/{track_id}/track-art.png")
    except Exception as e:
        pass

    session.commit()
    session.close()

    return track


def flag_track(track_id):
    session = get_session()

    track = session.query(Track).filter(Track.id == track_id).first()

    if track is None:
        return None

    track.flagged = True

    session.commit()
    session.close()

    return track


def unflag_track(track_id):
    session = get_session()

    track = session.query(Track).filter(Track.id == track_id).first()

    if track is None:
        return None

    track.flagged = None

    session.commit()
    session.close()

    return track


def delete_track(track_id):
    session = get_session()

    track = session.query(Track).filter(Track.id == track_id).first()

    if track is None:
        return None

    # Delete the track and all the Playlist, Album, Rating associated with it.
    playlists = get_track_playlists(track.id)
    for playlist in playlists:
        delete_playlist_item_by_playlist_track_id(playlist.playlist_id, track.id)

    albums = get_item_albums(track.id)
    for album_item in albums:
        delete_album_item(album_item.id)

    delete_track_ratings(track.id)
    delete_recent_by_track_id(track.id)

    delete_all_comments_by_track_id(track.id)

    delete_views_by_track_id(track.id)

    try:
        # Get all the files in the directory
        files = os.listdir(f"../media/tracks/{track_id}")
        # Delete all the files
        for file in files:
            os.remove(f"../media/tracks/{track_id}/{file}")
        # Delete the directory
        os.rmdir(f"../media/tracks/{track_id}")
    except Exception as e:
        pass


    session.delete(track)
    session.commit()
    session.close()

    return track


def get_track_dict(track):
    return {
        "id": track.id,
        "name": track.name,
        "lyrics": track.lyrics,
        "release_date": track.release_date,
        "duration": track.duration,
        "channel_id": track.channel_id,
        "genre_id": track.genre_id,
        "created_by": track.created_by,
        "last_modified_by": track.last_modified_by,
        "created_at": track.created_at,
        "last_modified_at": track.last_modified_at,
        "flagged": track.flagged,
        "channel": {
            "id": track.channel.id,
            "name": track.channel.name,
            "description": track.channel.description,
            "blacklisted": track.channel.blacklisted,
            "created_by": track.channel.created_by,
            "last_modified_by": track.channel.last_modified_by,
            "created_at": track.channel.created_at,
            "last_modified_at": track.channel.last_modified_at,
            "is_active": track.channel.is_active,
        },
    }


def search_tracks(keyword, count=10):
    return TrackSearch.query.filter(TrackSearch.name.match(keyword)).limit(count).all()
