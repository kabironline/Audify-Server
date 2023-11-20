from music.models import Track, Rating
from music.services.rating import get_rating_by_user_and_track_id
from membership.services.channel import get_channel_by_id
from core.db import get_session, get_db
from datetime import datetime
from werkzeug.datastructures import FileStorage
import os


def create_track(
    name, lyrics, release_date, media: FileStorage, track_art: FileStorage, channel_id
):
    """
    Creates a track with the given name, lyrics, release_date

    It performs the following tasks.

    - Checks if the media is a valid media file.
        - Only mp3 files are allowed.
    - Checks if the media file is not empty.

    In case of any validation failure, it raises an exception.

    The media will be uploaded to a "media/tracks/{track.id}/audio" folder and the
    media should be renamed into a uuid string.

    The database will store the uuid string of the media file.

    The track-art will be uploaded to a "media/tracks/{track-id}/track-art" folder and the
    track-art should be renamed into a uuid string.

    The database will store the uuid string of the track-art file.
    """

    session = get_session()

    track = Track(
        name=name,
        lyrics=lyrics,
        release_date=release_date,
        channel_id=channel_id,
        created_by=channel_id,
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
        os.mkdir(f"media/tracks/{track_id}")

        media.save(f"media/tracks/{track_id}/audio.mp3")
        track_art.save(f"media/tracks/{track_id}/track-art.png")
    except Exception as e:
        session.rollback()
        os.rmdir(f"media/tracks/{track_id}")
        raise e
    session.close()

    return track_id


def get_track_by_id(track_id, user_id=None, rating=False):
    session = get_session()

    track = session.query(Track).filter(Track.id == track_id).first()

    if rating:
        track.rating = get_rating_by_user_and_track_id(user_id, track.id)

    session.close()

    return track


def get_all_tracks():
    session = get_session()
    tracks = session.query(Track).all()
    session.close()

    return tracks


def get_tracks_by_channel(channel_id, user_id=None, rating=False, count=None):
    session = get_session()
    tracks = None
    if rating:
        tracks = (
            session.query(Track)
            .filter(Track.channel_id == channel_id)
            .order_by(Track.last_modified_at.desc())
        )
        for track in tracks:
            track.rating = get_rating_by_user_and_track_id(user_id, track.id)
    else:
        tracks = (
            session.query(Track)
            .filter(Track.channel_id == channel_id)
            .order_by(Track.last_modified_at.desc())
        )

    if count is not None:
        tracks = tracks.limit(count)
    else:
        tracks = tracks.all()

    session.close()

    return tracks


def get_top_rated_tracks(count=None):
    session = get_session()

    db = get_db()

    average_ratings = (
        db.session.query(Track, db.func.avg(Rating.rating).label("average_rating"))
        .join(Rating, Track.id == Rating.track_id)
        .group_by(Track.id)
        .order_by(db.func.avg(Rating.rating).desc())
    )

    if count is not None:
        average_ratings = average_ratings.limit(count)
    else:
        average_ratings = average_ratings.all()

    top_rated = []

    for track, average_rating in average_ratings:
        if average_rating is None or average_rating == 0:
            continue

        top_rated.append(track)

    session.close()

    return top_rated


def get_top_rated_channels(count=None):
    session = get_session()

    db = get_db()

    average_ratings = (
        db.session.query(Track, db.func.avg(Rating.rating).label("average_rating"))
        .distinct(Track.channel_id)
        .join(Rating, Track.id == Rating.track_id)
        .group_by(Track.channel_id)
        .order_by(db.func.avg(Rating.rating).desc())
    )

    if count is not None:
        average_ratings = average_ratings.limit(count)
    else:
        average_ratings = average_ratings.all()

    top_rated_channels = []
    for track, average_rating in average_ratings:
        if average_rating is None or average_rating == 0:
            continue

        top_rated_channels.append(get_channel_by_id(track.channel_id))

    session.close()

    return top_rated_channels


def get_latest_tracks(count=5):
    session = get_session()
    tracks = session.query(Track).order_by(Track.id.desc()).limit(count).all()
    session.close()

    return tracks


def update_track(
    track_id,
    name=None,
    lyrics=None,
    genre=None,
    release_date=None,
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

    try:
        if media is not None:
            media.save(f"media/tracks/{track_id}/audio.mp3")
        if track_art is not None:
            track_art.save(f"media/tracks/{track_id}/track-art.png")
    except Exception as e:
        pass

    session.commit()
    session.close()

    return track
