from werkzeug.datastructures import FileStorage
from datetime import datetime
from flask_restful import Resource, request
import music.services as services
import membership.services as membership_services
from flask import send_file
from flask_cors import cross_origin
import os


class TrackAPI(Resource):
    @cross_origin()
    def get(self, track_id):
        track = services.get_track_by_id(track_id)
        if track is None:
            return {"error": "Track not found"}, 404

        return {
            "track": services.get_track_dict(track),
            "action": "retrieved",
        }, 200

    @cross_origin()
    def post(self):
        # Reading the request body
        request_data = request.get_json()
        creator_name = request_data.get("creator_name")
        track_name = request_data.get("track_name")
        track_lyrics = request_data.get("track_lyrics")
        track_media = request_data.get("track_media")
        track_art = request_data.get("track_art")
        release_date = request_data.get("release_date")

        if creator_name is None:
            return {"error": "creator_name is required"}, 400

        creator = membership_services.get_channel_by_name(creator_name)
        if creator is None:
            return {"error": "creator not found"}, 404

        # Convert the release_date string into a datetime object
        release_date = datetime.strptime(release_date, "%Y-%m-%d")

        # Converting the path of the track_media and track_art into FileStorage objects
        track_media_file = open(track_media, "rb")
        track_media = FileStorage(track_media_file)

        track_art_file = open(track_art, "rb")
        track_art = FileStorage(track_art_file)

        services.create_track(
            name=track_name,
            release_date=release_date,
            lyrics="" if track_lyrics is None else track_lyrics,
            media=track_media,
            track_art=track_art,
            channel_id=creator.id,
        )

        track_art_file.close()
        track_media_file.close()

        return {"action": "Created"}, 201

    def put(self, track_id):
        # Reading the request body
        request_data = request.get_json()
        track_name = request_data.get("track_name")
        track_lyrics = request_data.get("track_lyrics")
        track_media = request_data.get("track_media")
        track_art = request_data.get("track_art")
        release_date = request_data.get("release_date")

        track = services.get_track_by_id(track_id)
        if track is None:
            return {"error": "Track not found"}, 404

        # Convert the release_date string into a datetime object
        release_date = datetime.strptime(release_date, "%Y-%m-%d")

        # Converting the path of the track_media and track_art into FileStorage objects
        track_media_file = open(track_media, "rb")
        track_media = FileStorage(track_media_file)

        track_art_file = open(track_art, "rb")
        track_art = FileStorage(track_art_file)

        services.update_track(
            track_id=track_id,
            name=track_name,
            release_date=release_date,
            lyrics="" if track_lyrics is None else track_lyrics,
            media=track_media,
            track_art=track_art,
        )

        track_art_file.close()
        track_media_file.close()

        return {"action": "Updated"}, 200

    def delete(self, track_id):
        track = services.get_track_by_id(track_id)
        if track is None:
            return {"error": "Track not found"}, 404

        services.delete_track(track_id)

        return {"action": "Deleted"}, 200