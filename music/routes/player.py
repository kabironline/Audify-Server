from flask import render_template, redirect, url_for, send_file, request
from music.services import *
from membership.services import get_user_by_id, get_channel_by_id
import core
import os


def player(track_id):
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    track = get_track_by_id(track_id)

    if track is None:
        return redirect(url_for("page_not_found"))

    if track.channel.blacklisted or track.channel.is_active is False:
        return redirect(url_for("home"))

    comments = get_comments_by_track_id(track_id)

    user = core.get_current_user()
    user_rating = get_rating_by_user_and_track_id(user.id, track_id)

    if user_rating is not None:
        user_rating = user_rating.rating

    track.user_rating = user_rating

    create_recent(user.id, track.id)
    create_new_view(track, user.id)

    track.views = get_views_by_track_id(track_id)

    return render_template(
        "music/player.html",
        track=track,
        artist=track.channel,
        comments=comments,
        current_user=user,
        average_rating=get_track_rating(track_id),
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
    track_cover_path = os.path.join(
        "..", "media", "tracks", str(track_id), "track-art.png"
    )
    return send_file(track_cover_path, mimetype="image/png")


def track_media(track_id):
    # Check if track exists
    track = get_track_by_id(track_id)
    if track is None:
        # TODO: Test this
        return "Track not found", 404

    track_media_path = os.path.join("..", "media", "tracks", str(track_id), "audio.mp3")
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
    id = int(route.split("id=")[1])

    track = get_track_by_id(id)

    for channel in user.channels:
        if channel["id"] == track.channel_id:
            delete_track(id)
            return redirect(route)
    return render_template("music/track_delete.html")


def track_flag():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif user.is_admin is False:
        return redirect(url_for("home"))

    route = request.form.get("route")
    id = int(route.split("id=")[1])

    track = get_track_by_id(id)

    if track.flagged is None:
        flag_track(track.id)

    return redirect(route)


def track_unflag(track_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif user.is_admin is False:
        return redirect(url_for("home"))

    track = get_track_by_id(track_id)

    unflag_track(track.id)

    return redirect(f'/{"/".join(request.referrer.split("/")[3:])}')


def player_list(album_id=None, playlist_id=None, position=0):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if album_id is None and playlist_id is None:
        return redirect(url_for("page_not_found"))

    list = []
    if album_id is not None:
        list = get_album_tracks_by_album_id(album_id)
        for item in list:
            item.views = get_views_by_track_id(item.id)

        if list == []:
            return redirect(url_for("album_page", album_id=album_id))

    elif playlist_id is not None:
        list = get_tracks_by_playlist_id(playlist_id)
        for item in list:
            item.views = get_views_by_track_id(item.id)

        if list == []:
            return redirect(url_for("playlist_page", playlist_id=playlist_id))

    if position >= len(list):
        position = 0

    create_recent(user.id, list[position].id)

    return render_template(
        "music/player_list.html",
        list=list,
        track=list[position],
        position=position,
        album_id=album_id,
        playlist_id=playlist_id,
    )


def track_edit(track_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    track = get_track_by_id(track_id)

    if track is None:
        return redirect(url_for("page_not_found"))

    is_creator = False
    for channel in user.channels:
        if channel["id"] == track.channel_id:
            is_creator = True
            break

    if not is_creator:
        return redirect(url_for("home"))

    if request.method == "POST":
        request_data = request.form
        name = request_data.get("title")
        lyrics = request_data.get("lyrics")
        release_date = request_data.get("release_date")
        genre_id = request_data.get("genre_id")

        release_date = datetime.strptime(release_date, "%Y-%m-%dT%H:%M")

        track_media = request.files.get("track_media")
        track_art = request.files.get("track_art")

        update_track(
            track_id,
            name=name,
            lyrics=lyrics,
            release_date=release_date,
            genre=genre_id,
            track_art=track_art,
            media=track_media,
        )

        track = get_track_by_id(track_id)
        genres = get_all_genres()
        return render_template("music/track_edit.html", track=track, genres=genres)

    genres = get_all_genres()
    return render_template("music/track_edit.html", track=track, genres=genres)
