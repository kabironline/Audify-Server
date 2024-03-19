from flask import render_template, request, redirect, url_for
import core
from membership.services import (
    deactivate_user,
    get_user_by_id,
    deactivate_channel,
    get_user_channels,
    get_channel_by_id,
    get_channel_dict,
)
from music.services import get_playlist_by_user, get_playlist_dict


def delete_user(user_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if user.id != user_id:
        return redirect(url_for("home"))

    if request.method == "POST":
        deactivate_user(user_id)
        return redirect(url_for("logout"))


def delete_channel(channel_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        deactivate_channel(channel_id)

        # Checking if user is a part of any channel
        members = get_user_channels(user.id)
        channel = None
        channels = []
        if len(members) != 0:
            for member in members:
                channel = get_channel_by_id(member.channel_id)
                if channel.is_active is False or channel.blacklisted:
                    continue
                channels.append(get_channel_dict(get_channel_by_id(member.channel_id)))
        if len(channels) == 0:
            channels = None
        playlist = []
        playlist_search = get_playlist_by_user(user.id)
        for playlist_item in playlist_search:
            playlist.append(get_playlist_dict(playlist_item))

        core.set_current_user(user, channels, playlist)

        return redirect(url_for("home"))
