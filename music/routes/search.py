from flask import render_template, redirect, url_for, request
import core
import music.services
import membership.services


def search():
    # get the q parameter from the url

    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    q = request.args.get("q")
    if q == "" or q is None:
        return render_template(
            "music/search.html",
            search_results_tracks=[],
            search_results_channels=[],
            search_results_playlists=[],
            search_results_albums=[],
            q=q,
        )

    track_search = music.services.track.search_tracks(q)
    track_results = []
    for track in track_search:
        track_temp = music.services.track.get_track_by_id(track.rowid)
        if track_temp.flagged or track_temp.channel.blacklisted:
            continue
        track_results.append(track_temp)

    channel_search = membership.services.channel.search_channels(q)

    playlist_results = []
    playlist_search = music.services.playlist.search_playlists(q)
    for playlist in playlist_search:
        playlist_temp = music.services.playlist.get_playlist_by_id(playlist.rowid)
        playlist_results.append(playlist_temp)

    album_results = []
    album_search = music.services.album.search_albums(q)
    for album in album_search:
        album_temp = music.services.album.get_album_by_id(album.rowid)
        if album_temp.channel.blacklisted:
            continue
        album_results.append(album_temp)

    if len(channel_search) > 0:
        # get some tracks from the channel
        for channel in channel_search:
            if len(track_results) <= 7:
                for track in music.services.track.get_tracks_by_channel(
                    channel.id, count=5
                ):
                    if track not in track_results:
                        track.channel = channel
                        track_results.append(track)
            if len(playlist_results) <= 7:
                for album in music.services.album.get_album_by_user(channel.id):
                    if album not in album_results:
                        album.channel = channel
                        album_results.append(album)

    return render_template(
        "music/search.html",
        search_results_tracks=track_results,
        search_results_channels=channel_search,
        search_results_playlists=playlist_results,
        search_results_albums=album_results,
        q=q,
    )
