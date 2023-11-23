from flask import render_template, redirect, url_for
import core
import music.services
import membership.services


def top_charts():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    top_rated = music.services.get_top_rated_tracks(count=12)
    for track in top_rated:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    top_charts = music.services.get_top_tracks(count=12)
    for track in top_charts:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    top_channels = music.services.get_top_rated_channels(count=12)
    return render_template(
        "music/top_charts.html",
        top_charts=top_charts,
        top_rated_charts=top_rated,
        top_creators=top_channels,
    )


def top_charts_tracks():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    top_rated = music.services.get_top_tracks(count=30)
    for track in top_rated:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    return render_template(
        "music/all_tracks.html", all_tracks=top_rated, title="Top Tracks"
    )


def top_rated_tracks():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    top_rated = music.services.get_top_rated_tracks(count=30)
    for track in top_rated:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    return render_template(
        "music/all_tracks.html", all_tracks=top_rated, title="Top Rated Tracks"
    )
