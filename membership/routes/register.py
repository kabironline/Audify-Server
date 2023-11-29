from flask import render_template, request, redirect, url_for
from membership.services import (
    create_user,
    get_user_by_username,
    create_channel,
    get_channel_by_name,
    create_member,
    get_channel_dict,
    update_channel,
    get_user_channels,
    get_channel_by_id,
)
from music.services import get_playlist_by_user, get_playlist_dict
import core


def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        nickname = request.form.get("nickname")
        bio = request.form.get("bio")

        # Checking for errors
        if get_user_by_username(username) is not None:
            return render_template(
                "membership/register.html",
                error="Username already taken, please choose another",
            )
        try:
            create_user(username, password, nickname, bio)
        except Exception as e:
            return render_template("membership/register.html", error=str(e))
        return redirect(url_for("login"))
    return render_template("membership/register.html")


def register_creator():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        request_data = request.form
        channel_name = request_data.get("name")
        channel_description = request_data.get("description")
        password = request_data.get("password")

        if password != user.password:
            return render_template(
                "membership/register_creator.html",
                error="Incorrect password, please try again",
            )

        create_channel(channel_name, channel_description)
        channel = get_channel_by_name(channel_name)
        create_member(user.id, channel.id)
        request_data = request.files
        avatar = request_data.get("avatar")

        if avatar is not None:
            update_channel(channel.id, channel_name, channel_description, avatar)

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

    return render_template("membership/register_creator.html", user=user)
