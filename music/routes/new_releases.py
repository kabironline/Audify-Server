from flask import render_template, redirect, url_for
import music.services
import membership.services
import core


def new_releases():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    new_releases = music.services.get_latest_tracks()
    for track in new_releases:
        track.channel = membership.services.get_channel_by_id(track.channel_id)
    return render_template("music/new_releases.html", new_releases=new_releases)


def new_releases_albums():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return render_template("music/new_releases_albums.html")


def new_releases_tracks():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    new_releases = music.services.get_latest_tracks(30)
    for track in new_releases:
        track.channel = membership.services.get_channel_by_id(track.channel_id)

    return render_template(
        "music/all_tracks.html", title="New Singles", all_tracks=new_releases
    )
