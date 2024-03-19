import music.services as music_services
import membership.services as membership_services
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource, request
from datetime import datetime
from werkzeug.datastructures import FileStorage

class TrackAPIV2(Resource):
  def get(self, track_id):
    track = music_services.get_track_by_id(track_id)
    if track is None:
      return {"error": "Track not found"}, 404
    
    return {
      "track": music_services.get_track_dict(track),
    }, 200
  @jwt_required()
  def post(self):
    request_data = request.form
    track_name = request_data.get("track_name")
    track_lyrics = request_data.get("track_lyrics")
    release_date = request_data.get("release_date")

    track_media = request.files.get("track_media")
    track_art = request.files.get("track_cover")
    
    creator = current_user.channel
    
    release_date = datetime.strptime(release_date, "%Y-%m-%d")

    music_services.create_track(
      name=track_name,
      release_date=release_date,
      lyrics="" if track_lyrics is None else track_lyrics,
      media=track_media,
      track_art=track_art,
      channel_id=creator.id,
    )

    return {"action": "created"}, 201
  
  def put(self, track_id):
    request_data = request.form
    track_name = request_data.get("track_name")
    track_lyrics = request_data.get("track_lyrics")
    track_media = request_data.get("track_media")

    track_art = request.form.get("track_art")
    release_date = request.form.get("release_date")
    track = music_services.get_track_by_id(track_id)
    if track is None:
      return {"error": "Track not found"}, 404
    
    release_date = datetime.strptime(release_date, "%Y-%m-%d")

    music_services.update_track(
      track_id,
      name=track_name,
      release_date=release_date,
      lyrics="" if track_lyrics is None else track_lyrics,
      media=track_media,
      track_art=track_art,
    )

    return {"action": "Updated"}, 200
  
  def delete(self, track_id):
    track = music_services.get_track_by_id(track_id)
    if track is None:
      return {"error": "Track not found"}, 404
    
    music_services.delete_track(track_id)

    return {"action": "Deleted"}, 200