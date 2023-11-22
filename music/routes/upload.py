from datetime import datetime
from flask import render_template, redirect, url_for, request
import core
from music.services import (
    create_track,
    get_tracks_by_channel,
    create_album,
    get_album_by_name,
    create_album_item,
)


def upload():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title")
        genre = request.form.get("genre")
        lyrics = request.form.get("lyrics")
        release_date = request.form.get("release_date")
        cover_art = request.files.get("cover")
        audio_file = request.files.get("track")

        create_track(
            name=title,
            lyrics=lyrics,
            release_date=release_date,
            media=audio_file,
            track_art=cover_art,
            user_id=core.get_current_user().id,
        )

        return redirect(url_for("home"))
    return render_template("music/upload.html")


def create_album_route():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title")
        release_date = request.form.get("release_date")
        description = request.form.get("description")
        cover_art = request.files.get("cover")
        tracks = request.form.getlist("tracks")

        # convert the str date to a datetime object
        release_date = datetime.strptime(release_date, "%Y-%m-%d")

        album = create_album(
            name=title,
            description=description,
            release_date=release_date,
            album_art=cover_art,
            channel_id=user.channels[0]["id"],
        )

        for track in tracks:
            create_album_item(album.id, track, user.channels[0]["id"])

        return redirect(url_for("home"))

    tracks = get_tracks_by_channel(user.channels[0]["id"])
    for track in tracks:
        track.channel = user.channels[0]

    if len(tracks) == 0:
        return redirect(url_for("upload"))

    return render_template("music/create_album.html", tracks=tracks)
