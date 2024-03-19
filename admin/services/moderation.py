from core.db import get_session
from admin.models import Whitelist
from membership.models import Channel
from music.models import Track
import membership.services
import music.services
from datetime import datetime


# --------------------------WhiteList--------------------------------


def create_whitelist(channel_id, created_by):
    session = get_session()
    whitelist = Whitelist(
        channel_id=channel_id,
        created_by=created_by,
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        last_modified_by=created_by,
    )
    session.add(whitelist)
    session.commit()
    session.close()
    return whitelist


def get_whitelist_by_channel_id(channel_id):
    session = get_session()
    whitelist = session.query(Whitelist).filter_by(channel_id=channel_id).first()
    session.close()
    return whitelist if whitelist else None


def get_whitelist():
    session = get_session()
    whitelist = (
        session.query(Channel).join(Whitelist, Channel.id == Whitelist.channel_id).all()
    )
    session.close()
    return whitelist


def delete_whitelist_by_channel_id(channel_id):
    session = get_session()
    whitelist = session.query(Whitelist).filter_by(channel_id=channel_id).first()
    session.delete(whitelist)
    session.commit()
    session.close()
    return whitelist if whitelist else None


# --------------------------BlackList--------------------------------


def create_blacklist(channel_id, user_id):
    session = get_session()
    channel = membership.services.get_channel_by_id(channel_id)
    # Checking if channel exists or is whitelisted
    if channel is None or get_whitelist_by_channel_id(channel_id):
        return None

    channel.blacklisted = True
    last_modified_by = user_id
    session.add(channel)
    session.commit()
    session.close()


def get_blacklist():
    session = get_session()
    channels = session.query(Channel).filter_by(blacklisted=True).all()
    session.close()
    return channels


def delete_blacklist(channel_id, user_id):
    session = get_session()
    channel = membership.services.get_channel_by_id(channel_id)
    channel.blacklisted = None
    channel.last_modified_by = user_id
    channel.last_modified_at = datetime.now()
    session.add(channel)
    session.commit()
    session.close()
    return channel if channel else None


# --------------------------Flagged--------------------------------


def create_track_flag(track_id, user_id):
    session = get_session()
    track = music.services.get_track_by_id(track_id)

    # Checking if the channel of the track is whitelisted
    if get_whitelist_by_channel_id(track.channel_id):
        return None

    track.flagged = True
    track.last_modified_by = user_id
    track.last_modified_at = datetime.now()
    session.add(track)
    session.commit()
    session.close()
    return track if track else None


def get_flagged_tracks():
    session = get_session()
    tracks = session.query(Track).filter_by(flagged=True).all()
    session.close()
    return tracks if tracks else None


def delete_track_flag(track_id, user_id):
    session = get_session()
    track = music.services.get_track_by_id(track_id)
    track.flagged = None
    track.last_modified_by = user_id
    track.last_modified_at = datetime.now()
    session.add(track)
    session.commit()
    session.close()
    return track if track else None
