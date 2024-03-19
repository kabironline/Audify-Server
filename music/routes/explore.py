from flask import render_template, redirect, url_for
import music.services
import membership.services
import core


def explore():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    from datetime import datetime

    timer = datetime.now()

    new_releases = music.services.get_latest_tracks()
    genres = music.services.get_all_genres()

    top_rated = music.services.get_top_rated_tracks(count=12)

    top_chart = music.services.get_top_tracks(count=12)

    print(datetime.now() - timer)

    return render_template(
        "music/explore.html",
        new_releases=new_releases,
        genres=genres,
        top_charts=top_chart,
        top_rated_tracks=top_rated,
    )
