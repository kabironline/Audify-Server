from flask import render_template, request, redirect, url_for
import membership.models
import music.models
import membership.services
import music.services
import core


def home():
    user = core.get_current_user()

    if user is None:
        return redirect(url_for("login"))

    carousel_title = "Recently Played"
    recents = music.services.get_recent_by_user_id(user.id)
    recently_played_tracks = []

    # Join the track table with the channel table
    # to get the artist name

    session = core.get_session()

    for recent in recents:
        track = music.services.get_track_by_id(recent.track_id)
        track.channel = membership.services.get_channel_by_id(track.channel_id)
        recently_played_tracks.append(track)

    session.close()
    latest_tracks = music.services.get_latest_tracks(5)
    for track in latest_tracks:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    for track in recently_played_tracks:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    latest_albums = music.services.get_latest_albums(5)
    for album in latest_albums:
        album.channel = membership.services.get_channel_by_id(album.created_by)

    return render_template(
        "music/home.html",
        recently_played=recently_played_tracks,
        carousel_title=carousel_title,
        latest_tracks=latest_tracks,
        latest_albums=latest_albums,
    )
