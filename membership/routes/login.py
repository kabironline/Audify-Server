from flask import render_template, request, redirect, url_for
from membership.services import (
    get_user_by_username,
    get_user_channels,
    get_channel_by_id,
    get_channel_dict,
)
from music.services import get_playlist_by_user, get_playlist_dict
import core


def login():
    if request.method in ["POST", "GET"] is False:  # return 405 method not allowed
        return

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username)
        print(password)

        if username is None or password is None:
            return render_template(
                "membership/login.html", error="Please fill all fields"
            )

        user = get_user_by_username(username)
        if user is None:
            return render_template("membership/login.html", error="User not found")
        elif user.password != password:
            return render_template(
                "membership/login.html", error="Password entered is incorrect"
            )
        elif user.is_active is False:
            return render_template(
                "membership/login.html", error="User account deactivated"
            )

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
    return render_template("membership/login.html")


def logout():
    core.logout()
    return redirect(url_for("login"))
