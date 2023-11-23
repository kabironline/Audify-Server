from flask import render_template, request, redirect, url_for
from music.services import (
    get_all_tracks,
    get_all_genres,
    get_all_albums,
    get_all_playlists,
)
import core


def admin_dashboard():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    tracks = get_all_tracks()

    genres = get_all_genres()

    albums = get_all_albums()

    playlists = get_all_playlists()

    render_template("admin/dashboard.html", user=user)
