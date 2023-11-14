from flask import render_template, redirect, url_for, send_file
from music.services import get_track_by_id, get_comments_by_track_id
from membership.services import get_user_by_id
import core
import music.services


def player(track_id):
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    track = get_track_by_id(track_id)
    artist = get_user_by_id(track.created_by)
    comments = get_comments_by_track_id(track_id)
    # joining the comments with the users who created them
    for comment in comments:
        comment.user = get_user_by_id(comment.user_id)

    user = core.get_current_user()
    user_rating = music.services.get_rating_by_user_and_track_id(
        track_id, user.id
    ).rating

    track.user_rating = user_rating

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
