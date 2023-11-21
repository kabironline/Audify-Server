from flask import render_template, redirect, url_for, request
import core
import music.services
import membership.services


def search():
    # get the q parameter from the url
    q = request.args.get("q")

    track_search = music.services.track.search_tracks(q)
    track_results = []
    for track in track_search:
        track_temp = music.services.track.get_track_by_id(track.rowid)
        track_temp.channel = membership.services.channel.get_channel_by_id(
            track_temp.channel_id
        )
        track_results.append(track_temp)

    channel_search = membership.services.channel.search_channels(q)

    return render_template(
        "music/search.html",
        search_results_tracks=track_results,
        search_results_channels=channel_search,
        # q=q,
    )
