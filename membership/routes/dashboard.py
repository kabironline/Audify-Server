from flask import render_template, request, redirect, url_for
from membership.services import get_user_by_id, get_channel_by_id, get_channel_members
import music.services
import core


def dashboard(user_id=None):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    user_id = user.id if user_id is None else user_id
    user = get_user_by_id(user_id) if user_id is not user.id else user

    recent_tracks = music.services.get_recent_by_user_id(user_id)

    for i in range(len(recent_tracks)):
        recent_tracks[i] = music.services.get_track_by_id(recent_tracks[i].track_id)
        recent_tracks[i].channel = get_channel_by_id(recent_tracks[i].channel_id)
        rating = music.services.get_rating_by_user_and_track_id(
            user_id, recent_tracks[i].id
        )

        if rating is not None:
            recent_tracks[i].rating = rating.rating

    playlists = music.services.get_playlist_by_user(user_id)
    for playlist in playlists:
        playlist.created_by = user

        return render_template(
            "membership/dashboard.html",
            user=user,
            own_profile=False,
            recent_tracks=recent_tracks,
            playlists=playlists,
        )


def dashboard_channel(channel_id=None):
    channel = get_channel_by_id(channel_id)
    user = core.get_current_user()

    if user is None:
        return redirect(url_for("login"))

    # Check if the user is a member of the channel
    is_member = any(
        [member.user_id == user.id for member in get_channel_members(channel_id)]
    )

    if channel is None:
        # TODO: Redirect to 404 page
        return redirect(url_for("home"))

    channel_tracks = music.services.get_tracks_by_channel(channel_id)
    for track in channel_tracks:
        track.channel = channel

    # TODO: Add Album and Playlist information to the channel

    return render_template(
        "membership/dashboard_channel.html",
        channel=channel,
        own_profile=is_member,
        channel_tracks=channel_tracks,
    )


def dashboard_channel_tracks(channel_id=None):
    channel = get_channel_by_id(channel_id)

    if channel is None:
        # TODO: Redirect to 404 page
        return redirect(url_for("home"))

    channel_tracks = music.services.get_tracks_by_channel(channel_id)
    for track in channel_tracks:
        track.channel = channel

    return render_template(
        "music/all_tracks.html", all_tracks=channel_tracks, title=channel.name
    )
