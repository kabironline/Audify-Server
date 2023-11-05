from flask import render_template, redirect, url_for
import core


def new_releases():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return render_template("music/new_releases.html")


def new_releases_albums():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return render_template("music/new_releases_albums.html")


def new_releases_tracks():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return render_template("music/new_releases_tracks.html")
