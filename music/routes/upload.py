from flask import render_template, redirect, url_for, request
import core
from music.services import create_track


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
