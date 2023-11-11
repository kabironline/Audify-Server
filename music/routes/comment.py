from flask import render_template, redirect, url_for, request
from music.services.comment import create_comment, delete_comment
import core


def post_comment_route(track_id):
    if request.method != "POST":
        return redirect(url_for("player", track_id=track_id))

    if core.get_current_user() is None:
        return redirect(url_for("login"))

    comment = request.form.get("comment")
    track_id = track_id
    user_id = core.get_current_user().id

    create_comment(comment, track_id, user_id)

    return redirect(url_for("player", track_id=track_id))


def delete_comment_route(track_id, comment_id):
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    delete_comment(comment_id)

    return redirect(url_for("player", track_id=track_id))
