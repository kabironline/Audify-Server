from flask import render_template, request, redirect, url_for
from membership.services import get_user_by_id, get_channel_by_id
import music.services
import core


def dashboard(user_id=None):
    user = core.get_current_user()

    user_id = user.id if user_id is None else user_id

    recent_tracks = music.services.get_recent_by_user_id(user_id)

    for i in range(len(recent_tracks)):
        recent_tracks[i] = music.services.get_track_by_id(recent_tracks[i].track_id)
        recent_tracks[i].channel = get_channel_by_id(recent_tracks[i].channel_id)
        rating = music.services.get_rating_by_user_and_track_id(
            user_id, recent_tracks[i].id
        )

        if rating is not None:
            recent_tracks[i].rating = rating.rating

    if user is None:
        return redirect(url_for("login"))
    if user_id is None or user_id == user.id:
        return render_template(
            "membership/dashboard.html",
            user=user,
            recent_tracks=recent_tracks,
            own_profile=True,
        )
    else:
        user = get_user_by_id(user_id)

        return render_template(
            "membership/dashboard.html",
            user=user,
            own_profile=False,
            recent_tracks=recent_tracks,
        )
