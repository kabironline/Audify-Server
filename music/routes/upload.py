from flask import render_template, redirect, url_for, request
import core
from music.services import create_track


def upload():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        # Get all the data from the form
        title = request.form.get("title")
        genre = request.form.get("genre")
        lyrics = request.form.get("lyrics")
        release_date = request.form.get("release_date")
        cover_art = request.files.get("cover")
        audio_file = request.files.get("track")

        create_track(
            title,
            lyrics,
            release_date,
            audio_file,
            cover_art,
            core.get_current_user().id,
        )

        return redirect(url_for("home"))
    return render_template("music/upload.html")
