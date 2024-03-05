from flask_restful import Resource, request
from music.services import get_latest_tracks, get_track_dict, get_latest_albums, get_album_dict, get_latest_playlist,get_playlist_dict, get_track_rating_for_user
from flask_jwt_extended import jwt_required, current_user
class LatestAPI(Resource):
  @jwt_required(optional=True)
  def get(self):
    # Check the route if it has "tracks" or "albums"
    route = request.path.split("/")[3]
    if route == "albums":
      latest = get_latest_albums()
      latest_json = [(get_album_dict(album)) for album in latest]
      return {
        "latest": latest_json,
      }, 200
    elif route == "tracks":
      latest = get_latest_tracks()
      
      if request.headers.get("Authorization"):
        ratings = get_track_rating_for_user(current_user.id, *[latest_track.id for latest_track in latest])
        for track in latest:
          track.rating = ratings.get(track.id, None)
      latest_json = [(get_track_dict(track)) for track in latest]
      return {
        "latest": latest_json,
      }, 200
    
    elif route == "playlists":
      latest = get_latest_playlist()
      latest_json = [(get_playlist_dict(playlist)) for playlist in latest]
      return {
        "latest": latest_json,
      }, 200