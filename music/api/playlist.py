from flask_restful import Resource, request
import music.services as music_services
import membership.services as membership_services
from flask_jwt_extended import jwt_required, current_user

class PlaylistAPI(Resource):
  @jwt_required(optional=True)
  def get(self, playlist_id=None, user_id=None):
    if playlist_id is not None:
      playlist = music_services.get_playlist_by_id(playlist_id)
      playlist_items = music_services.get_tracks_by_playlist_id(playlist_id)
      if playlist is None:
        return {"error": "Playlist not found"}, 404
    
      auth = request.headers.get("Authorization")
      if auth:
        user_id = current_user.id
        ratings = music_services.get_track_rating_for_user(user_id, *[playlist_item.id for playlist_item in playlist_items])
        for track in playlist_items:
          track.rating = ratings.get(track.id, None)
      playlist_dict = music_services.get_playlist_dict(playlist)
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


  def put(self, playlist_id):
    request_data = request.get_json()
    playlist_name = request_data.get("playlist_name")
    playlist_description = request_data.get("playlist_description")
    playlist_tracks = request_data.get("playlist_tracks")
    user_id = request_data.get("user_id")

    if user_id is None:
      return {"error": "User ID is required"}, 400
    
    user = membership_services.get_user_by_id(user_id)
    if user is None:
      return {"error": "User not found"}, 404
    
    playlist = music_services.get_playlist_by_id(playlist_id)
    
    if playlist is None:
      return {"error": "Playlist not found"}, 404
    
    music_services.update_playlist(
      playlist_id,
      name=playlist_name,
      description=playlist_description,
    )

    if playlist_tracks is not None:
      music_services.delete_playlist_item(playlist_id)
      for track_id in playlist_tracks:
        music_services.create_playlist_item(
          playlist_id=playlist.id,
          track_id=track_id,
          user_id=user.id,
        )

    return {
      "action": "updated",
    }, 201
  @jwt_required()
  def delete(self, playlist_id):
    
    playlist = music_services.get_playlist_by_id(playlist_id)

    if playlist is None:
      return {"error": "Playlist not found"}, 404
    
    if playlist.user.id != current_user.id:
      return {"error": "Unauthorized"}, 401
    
    music_services.delete_playlist(playlist_id, user_id=current_user.id)
    
    return {
      "action": "deleted",
    }, 200


    