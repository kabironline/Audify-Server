from datetime import datetime
from flask import render_template, redirect, url_for, request
import core
from music.services import create_track, get_all_genres


def upload():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title")
        genre = request.form.get("genre")
        lyrics = request.form.get("lyrics")
        release_date = request.form.get("release_date")
        cover_art = request.files.get("cover")
        audio_file = request.files.get("track")

        release_date = datetime.strptime(release_date, "%Y-%m-%d")

        create_track(
            name=title,
            lyrics=lyrics,
            release_date=release_date,
            media=audio_file,
            track_art=cover_art,
            channel_id=user.channels[0]["id"],
            genre_id=genre,
        )

        return redirect(url_for("home"))

    genres = get_all_genres()

    return render_template("music/upload.html", genres=genres)
