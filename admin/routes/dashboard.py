from flask import render_template, request, redirect, url_for, send_file
from music.services import (
    get_all_tracks,
    get_all_genres,
    get_all_albums,
    get_all_playlists,
)
from membership.services import get_all_channels, get_all_users, get_user_by_id
from admin.services import *
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

    blacklisted_channels = get_blacklist()

    whitelisted_channels = get_whitelist()

    return render_template(
        "admin/dashboard.html",
        user=user,
        tracks=tracks,
        genres=genres,
        albums=albums,
        playlists=playlists,
        users=users,
        channels=channels,
        blacklisted_channels=blacklisted_channels,
        whitelisted_channels=whitelisted_channels,
        genre_distribution_graph=generate_genre_distribution_graph(),
        user_channel_distribution_graph=generate_user_channel_distribution_graph(),
        genre_listener_graph=generate_genre_listener_graph(),
        viewership_graph=generate_recent_viewership_graph(),
    )


def admin_dashboard_blacklist():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    blacklisted_channels = get_blacklist()
    for channel in blacklisted_channels:
        channel.blacklisted_by = get_user_by_id(channel.last_modified_by)

    return render_template(
        "admin/blacklisted.html",
        user=user,
        blacklisted_channels=blacklisted_channels,
    )


def admin_dashboard_whitelist():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    whitelisted_channels = get_whitelist()
    for channel in whitelisted_channels:
        channel.whitelisted_by = get_user_by_id(channel.last_modified_by)

    return render_template(
        "admin/whitelisted.html",
        user=user,
        whitelisted_channels=whitelisted_channels,
    )


def admin_dashboard_tracks():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    tracks = get_all_tracks()

    return render_template(
        "music/all_tracks_list.html",
        all_tracks=tracks,
        edit=False,
    )
