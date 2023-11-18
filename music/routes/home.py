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
    recents = music.services.get_recent_by_user_id(user.id)
    recently_played_tracks = []

    # Join the track table with the channel table
    # to get the artist name

    session = core.get_session()

    for recent in recents:
        track = music.services.get_track_by_id(recent.track_id)
        track.channel = (
            session.query(membership.models.Channel)
            .filter_by(id=track.channel_id)
            .first()
        )
        recently_played_tracks.append(track)

    return render_template("music/home.html", recently_played=recently_played_tracks)
