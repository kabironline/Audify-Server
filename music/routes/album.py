from flask import render_template, redirect, url_for, send_file, request
from music.services import *
from membership.services import get_user_by_id, get_channel_by_id
import core
import os


def album_page(album_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    album = get_album_by_id(album_id)
    if album is None:
        return redirect(url_for("home"))
    album.items = get_album_tracks_by_album_id(album_id)

    ratings = get_track_rating_for_user(user.id, *[item.id for item in album.items])

    for album_item in album.items:
        album_item.rating = ratings[album_item.id] if album_item.id in ratings else None

    return render_template(
        "music/album.html",
        album=album,
        artist=album.channel,
    )


def create_album_route():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title")
        release_date = request.form.get("release_date")
        description = request.form.get("description")
        cover_art = request.files.get("cover")
        tracks = request.form.getlist("tracks")

        # convert the str date to a datetime object
        release_date = datetime.strptime(release_date, "%Y-%m-%d")

        album = create_album(
            name=title,
            description=description,
            release_date=release_date,
            album_art=cover_art,
            channel_id=user.channels[0]["id"],
        )

        for track in tracks:
            create_album_item(album.id, track, user.channels[0]["id"])

        return redirect(url_for("home"))

    tracks = get_tracks_by_channel(user.channels[0]["id"], count=10000)
    for track in tracks:
        track.channel = user.channels[0]

    if len(tracks) == 0:
        return redirect(url_for("upload"))

    return render_template("music/album_create.html", tracks=tracks)


def album_update_route(album_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    album = get_album_by_id(album_id)

    if request.method == "POST":
        is_author = False
        for channel in user.channels:
            if channel["id"] == album.created_by:
                is_author = True
                break
        if not is_author:
            return url_for("album_page", album_id=album_id)

        album_name = request.form.get("name")
        album_description = request.form.get("description")
        album_cover = request.files.get("cover")
        release_date = request.form.get("release_date")
        tracks = request.form.getlist("tracks")

        release_date = (
            datetime.strptime(release_date, "%Y-%m-%d") if release_date != "" else None
        )

        update_album(album_id, album_name, album_description, release_date, album_cover)

        updated_tracks = request.form.getlist("tracks")
        if updated_tracks is None or len(updated_tracks) == 0:
            return redirect(url_for("album_page", album_id=album_id))

        # delete all the tracks from the album
        album_items = get_album_items_by_album_id(album_id)
        for album_item in album_items:
            delete_album_item(album_item.id)

        # add the new tracks to the album
        for track in updated_tracks:
            create_album_item(album_id, track, user.channels[0]["id"])

        return redirect(url_for("album_page", album_id=album_id))

    tracks = get_tracks_by_channel(user.channels[0]["id"], count=10000)
    for track in tracks:
        track.channel = user.channels[0]

    items = get_album_tracks_by_album_id(album_id)
    item_list = []
    for item in items:
        item_list.append(item.id)

    album.items = item_list

    if len(tracks) == 0:
        return redirect(url_for("upload"))

    album.release_date = album.release_date.strftime("%Y-%m-%d")

    return render_template(
        "music/album_update.html",
        tracks=tracks,
        album=album,
    )


def album_delete_route(album_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    album = get_album_by_id(album_id)

    is_author = False
    channel_id = 0
    for channel in user.channels:
        if channel["id"] == album.created_by:
            is_author = True
            channel_id = channel["id"]
            break
    if not is_author:
        return url_for("album_page", album_id=album_id)

    delete_album(album_id, channel_id)

    return redirect(url_for("home"))


def album_cover(album_id):
    # Check if album exists
    album = get_album_by_id(album_id)
    if album is None:
        # TODO: Test this
        return "Album not found", 404

    album_cover_path = os.path.join(
        "..", "media", "albums", str(album_id), "album_art.png"
    )
    return send_file(album_cover_path, mimetype="image/png")
