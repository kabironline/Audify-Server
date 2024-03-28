from flask_restful import Resource, request
import music.services as music_services
import membership.services as membership_services
from flask_jwt_extended import jwt_required, current_user
from core.db import get_redis
import json 
class PlaylistAPI(Resource):
  @jwt_required(optional=True)
  def get(self, playlist_id=None, user_id=None):
    if playlist_id is not None:
      r = get_redis()
      playlist = None
      if r.get(f"playlist:{playlist_id}") is not None:
        playlist_dict = json.loads(r.get(f"playlist:{playlist_id}"))
      else: 
        playlist = music_services.get_playlist_by_id(playlist_id)
        playlist_dict = music_services.get_playlist_dict(playlist)
      
      playlist_items = music_services.get_tracks_by_playlist_id(playlist_id)
      if playlist is None and playlist_dict is None:
        return {"error": "Playlist not found"}, 404
    
      auth = request.headers.get("Authorization")
      if auth:
        user_id = current_user.id
        ratings = music_services.get_track_rating_for_user(user_id, *[playlist_item.id for playlist_item in playlist_items])
        for track in playlist_items:
          track.rating = ratings.get(track.id, None)
      
      if r.get(f"playlist:{playlist_id}") is None:
        r.set(f"playlist:{playlist_id}", json.dumps(playlist_dict), ex=3600)
      playlist_dict["tracks"] = [music_services.get_track_dict(track) for track in playlist_items]
      return {
        "playlist": playlist_dict,
      }, 200
    
    elif user_id is not None:
      # Get all playlists for a user
      playlists = music_services.get_playlist_by_user(user_id)
      return {
        "playlists": [music_services.get_playlist_dict(playlist) for playlist in playlists],
      }, 200
    
  @jwt_required()
  def post(self):
    request_data = request.get_json()
    playlist_name = request_data.get("playlist_name")
    playlist_description = request_data.get("playlist_description")
    user = current_user
    
    playlist = music_services.create_playlist(
      name=playlist_name,
      description=playlist_description,
      user_id=user.id,
      api=True,
    )

    return {
      "action": "created",
      "playlist": music_services.get_playlist_dict(playlist),
    }, 201

  @jwt_required()
  def put(self, playlist_id):
    request_data = request.get_json()
    playlist_name = request_data.get("playlist_name")
    playlist_description = request_data.get("playlist_description")
    user = current_user

    playlist = music_services.get_playlist_by_id(playlist_id)

    if playlist.user.id != user.id:
      return {"error": "Unauthorized"}, 401
    
    if playlist is None:
      return {"error": "Playlist not found"}, 404

    playlist = music_services.update_playlist(
      playlist_id,
      name=playlist_name,
      description=playlist_description,
      user_id=user.id,
    )

    r = get_redis()
    r.delete(f"playlist:{playlist_id}")
    r.set(f"playlist:{playlist_id}", json.dumps(music_services.get_playlist_dict(playlist)), ex=3600)

    return {
      "action": "updated",
      "playlist": music_services.get_playlist_dict(playlist),
    }, 201

  @jwt_required()
  def delete(self, playlist_id):
    
    playlist = music_services.get_playlist_by_id(playlist_id)

    if playlist is None:
      return {"error": "Playlist not found"}, 404
    
    if playlist.user.id != current_user.id:
      return {"error": "Unauthorized"}, 401
    
    music_services.delete_playlist(playlist_id, user_id=current_user.id)
    r = get_redis()
    r.delete(f"playlist:{playlist_id}")
    return {
      "action": "deleted",
    }, 200


    