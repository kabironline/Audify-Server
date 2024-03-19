from flask import render_template, redirect, url_for
import music.services
import membership.services
import core


def new_releases():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    new_releases = music.services.get_latest_tracks()

    new_releases_albums = music.services.get_latest_albums()

    return render_template(
        "music/new_releases.html",
        new_releases=new_releases,
        new_releases_albums=new_releases_albums,
    )


def new_releases_albums():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    latest_albums = music.services.get_latest_albums(30)

    return render_template(
        "music/new_releases_albums.html", latest_albums=latest_albums
    )


def new_releases_tracks():
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    new_releases = music.services.get_latest_tracks(30)

    return render_template(
        "music/all_tracks.html", title="New Singles", all_tracks=new_releases
    )
