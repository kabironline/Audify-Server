from flask import render_template, redirect, url_for, request
import music.services
import membership.services
import core
import music.services


def update_rating(track_id, rating):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if user.is_active is False:
        return redirect(url_for("home"))

    music.services.create_or_update_rating(track_id, user.id, rating)

    return redirect(f"/{'/'.join(request.referrer.split('/')[3:])}")
