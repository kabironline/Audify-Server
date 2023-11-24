from flask import render_template, request, redirect, url_for, send_file
from music.services import (
    get_all_tracks,
    get_all_genres,
    get_all_albums,
    get_all_playlists,
)
from membership.services import get_all_channels, get_all_users
from admin.services import (
    generate_genre_distribution_graph,
    generate_user_channel_distribution_graph,
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

    users = get_all_users()

    channels = get_all_channels()

    return render_template(
        "admin/dashboard.html",
        user=user,
        tracks=tracks,
        genres=genres,
        albums=albums,
        playlists=playlists,
        users=users,
        channels=channels,
    )


def genre_distribution_graph():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    return generate_genre_distribution_graph()


def user_channel_distribution_graph():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    return generate_user_channel_distribution_graph()
