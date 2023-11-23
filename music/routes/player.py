from flask import render_template, redirect, url_for, send_file, request
from music.services import *
from membership.services import get_user_by_id, get_channel_by_id
import core
import music.services


def player(track_id):
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    track = get_track_by_id(track_id)
    artist = get_channel_by_id(track.created_by)
    comments = get_comments_by_track_id(track_id)
    # joining the comments with the users who created them
    for comment in comments:
        comment.user = get_user_by_id(comment.user_id)

    user = core.get_current_user()
    user_rating = music.services.get_rating_by_user_and_track_id(user.id, track_id)

    if user_rating is not None:
        user_rating = user_rating.rating

    track.user_rating = user_rating

    create_recent(user.id, track_id)

    return render_template(
        "music/player.html",
        track=track,
        artist=artist,
        comments=comments,
        current_user=user,
        average_rating=music.services.get_track_rating(track_id),
    )


def track(track_id):
    # Check if track exists
    track = get_track_by_id(track_id)
    if track is None:
        # TODO: Test this
        return "Track not found", 404

    track_path = "media/tracks/" + str(track_id) + "/audio.mp3"
    track_cover_path = "media/tracks/" + str(track_id) + "/track-art.png"
    return send_file(track_path, mimetype="audio/mpeg"), send_file(
        track_cover_path, mimetype="image/png"
    )


def track_cover(track_id):
    # Check if track exists
    track = get_track_by_id(track_id)
    if track is None:
        # TODO: Test this
        return "Track not found", 404

    track_cover_path = "media/tracks/" + str(track_id) + "/track-art.png"
    return send_file(track_cover_path, mimetype="image/png")


def track_media(track_id):
    # Check if track exists
    track = get_track_by_id(track_id)
    if track is None:
        # TODO: Test this
        return "Track not found", 404

    track_media_path = "media/tracks/" + str(track_id) + "/audio.mp3"
    return send_file(track_media_path, mimetype="audio/mpeg")


def player_controls():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    return render_template("music/player_controls.html")


def track_delete():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    route = request.form.get("route")
    id = int(route.split("=")[1])

    track = get_track_by_id(id)

    for channel in user.channels:
        if channel["id"] == track.channel_id:
            delete_track(id)
            return redirect(route)
    return render_template("music/track_delete.html")


def player_list(album_id=None, playlist_id=None, position=0):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if album_id is None and playlist_id is None:
        return redirect(url_for("home"))

    list = []
    if album_id is not None:
        items = get_album_items_by_album_id(album_id)
        for item in items:
            track = get_track_by_id(item.track_id)
            track.channel = get_channel_by_id(track.created_by)
            list.append(track)

    elif playlist_id is not None:
        items = get_playlist_items_by_playlist_id(playlist_id)
        for item in items:
            track = get_track_by_id(item.track_id)
            track.channel = get_channel_by_id(track.created_by)
            list.append(track)

    return render_template(
        "music/player_list.html",
        list=list,
        track=list[position],
        position=position,
        album_id=album_id,
        playlist_id=playlist_id,
    )
