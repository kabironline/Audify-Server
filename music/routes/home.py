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
    recently_played_tracks = music.services.get_recent_by_user_id(user.id)

    latest_tracks = music.services.get_latest_tracks(5)

    latest_albums = music.services.get_latest_albums(5)

    latest_playlists = music.services.get_latest_playlist(5)


    return render_template(
        "music/home.html",
        recently_played=recently_played_tracks,
        carousel_title=carousel_title,
        latest_tracks=latest_tracks,
        latest_albums=latest_albums,
        latest_playlists=latest_playlists,
    )
