from flask import render_template, redirect, url_for
import music.services
import membership.services
import core


def genre_tracks(genre_id):
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    genre = music.services.get_genre_by_id(genre_id)
    tracks = music.services.get_genre_tracks(genre_id)
    for track in tracks:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    return render_template("music/all_tracks.html", title=genre.name, all_tracks=tracks)
