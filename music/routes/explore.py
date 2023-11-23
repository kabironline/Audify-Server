from flask import render_template, redirect, url_for
import music.services
import membership.services
import core


def explore():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    new_releases = music.services.get_latest_tracks()
    for track in new_releases:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    genres = music.services.get_all_genres()
    from datetime import datetime

    top_rated = music.services.get_top_rated_tracks(count=12)
    for track in top_rated:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    top_chart = music.services.get_top_tracks(count=12)
    for track in top_chart:
        track.channel = membership.services.get_channel_by_id(track.channel_id)


    return render_template(
        "music/explore.html",
        new_releases=new_releases,
        genres=genres,
        top_charts=top_chart,
        top_rated_tracks=top_rated,
    )
