from music.services import *
from membership.services import (
    get_user_by_id,
    get_channel_by_id,
    get_user_channels,
    get_channel_dict,
)
from flask import render_template, redirect, url_for, request
import core
import datetime


def playlist_page(playlist_id=None):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        route = request.form.get("route")
        playlist = create_playlist(name, description)

        # Checking if user is a part of any channel
        members = get_user_channels(user.id)
        channel = None
        if len(members) != 0:
            channel = []
            for member in members:
                channel.append(get_channel_dict(get_channel_by_id(member.channel_id)))

        playlist = []
        playlist_search = get_playlist_by_user(user.id)
        for playlist_item in playlist_search:
            playlist.append(get_playlist_dict(playlist_item))

        core.set_current_user(user, channel, playlist)

        return redirect(route)

    timer = datetime.datetime.now()
    playlist = get_playlist_by_id(playlist_id)
    
    if playlist is None:
        return redirect(url_for("home"))
    playlist.items = get_playlist_items_by_playlist_id(playlist_id)

    ratings = get_track_rating_for_user(user.id, *[item.id for item in playlist.items])
    for item in playlist.items:
        item.rating = ratings[item.id] if item.id in ratings else None

    playlist.author = get_user_by_id(playlist.created_by)

    print(datetime.datetime.now() - timer)
    return render_template(
        "music/playlist.html", playlist_id=playlist_id, playlist=playlist
    )


def playlist_update(playlist_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    name = request.form.get("name")
    description = request.form.get("description")

    update_playlist(playlist_id, name, description)

    # Checking if user is a part of any channel
    members = get_user_channels(user.id)
    channel = None
    if len(members) != 0:
        channel = []
        for member in members:
            channel.append(get_channel_dict(get_channel_by_id(member.channel_id)))

    playlist = []
    playlist_search = get_playlist_by_user(user.id)
    for playlist_item in playlist_search:
        playlist.append(get_playlist_dict(playlist_item))

    core.set_current_user(user, channel, playlist)

    return redirect(url_for("playlist_page", playlist_id=playlist_id))


def playlist_delete(playlist_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    delete_playlist(playlist_id, user.id)
    # Checking if user is a part of any channel
    members = get_user_channels(user.id)
    channel = None
    if len(members) != 0:
        channel = []
        for member in members:
            channel.append(get_channel_dict(get_channel_by_id(member.channel_id)))

    playlist = []
    playlist_search = get_playlist_by_user(user.id)
    for playlist_item in playlist_search:
        playlist.append(get_playlist_dict(playlist_item))

    core.set_current_user(user, channel, playlist)
    return redirect(url_for("home"))


def playlist_add():
    route = request.form.get("route")
    playlist_ids = request.form.getlist("playlist")
    track_id = int(route.split("=")[-1])

    for playlist_id in playlist_ids:
        create_playlist_item(int(playlist_id), track_id, core.get_current_user().id)

    return redirect(route.split("?")[0])


def playlist_track_delete(playlist_id, track_id):
    delete_playlist_item_by_playlist_track_id(playlist_id, track_id)
    return redirect(url_for("playlist_page", playlist_id=playlist_id))


def update_playlist_track_rating(track_id, rating, playlist_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    create_or_update_rating(track_id, user.id, rating)

    return redirect(url_for("playlist_page", playlist_id=playlist_id))
