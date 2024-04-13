import music.services as music_services
import membership.services as membership_services
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime
from core.db import get_redis
import json
from flask_restful import Resource, request

class TrackAPIV2(Resource):
  def get(self, track_id):
    track = music_services.get_track_by_id(track_id)
    if track is None:
      return {"error": "Track not found"}, 404
    r = get_redis()    
    if r.get(f'track-{track_id}'):
      return json.loads(r.get(f'track-{track_id}')), 200
    final_json = {
      "track": music_services.get_track_dict(track),
    }
    r.set(f'track-{track_id}', json.dumps(final_json))
    return final_json , 200
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

    r = get_redis()
    r.delete(f'track-{track_id}')

    return {"action": "Updated"}, 200
  
  @jwt_required()
  def delete(self, track_id):
    track = music_services.get_track_by_id(track_id)
    if track is None:
      return {"error": "Track not found"}, 404
    
    if track.channel_id != current_user.channel.id:
      return {"error": "You are not the owner of the track"}, 403
    
    music_services.delete_track(track_id)

    r = get_redis()
    # clear all caches where this track is used
    r.delete(f'track-{track_id}')
    
    if track_in_cache(track_id, "latest-tracks-5"):
      r.delete("latest-tracks-5")
    if track_in_cache(track_id, "latest-tracks-30"):
      r.delete("latest-tracks-30")
    if track_in_cache(track_id, "top-tracks-16"):
      r.delete("top-tracks-16")
    if track_in_cache(track_id, "top-tracks-30"):
      r.delete("top-tracks-30")
    if track_in_cache(track_id, "top-rated-tracks-16"):
      r.delete("top-rated-tracks-16")
    if track_in_cache(track_id, "top-rated-tracks-30"):
      r.delete("top-rated-tracks-30")

    r.delete(f"genre-{track.genre_id}-tracks")
    return {"action": "Deleted"}, 

def track_in_cache(track_id, cache):
  r = get_redis()
  if not r.get(cache):
    return False
  tracks = json.loads(r.get(cache))
  # check for the track in the tracks list 
  for track in tracks["tracks"]:
    if track["id"] == track_id:
      return True
  return False
