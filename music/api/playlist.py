from flask_restful import Resource, request
import music.services as music_services
import membership.services as membership_services

class PlaylistAPI(Resource):
  def get(self, playlist_id):
    playlist = music_services.get_playlist_by_id(playlist_id)
    if playlist is None:
      return {"error": "Playlist not found"}, 404
    
    return {
      "playlist": music_services.get_playlist_dict(playlist),
    }, 200
  
  def post(self):
    request_data = request.get_json()
    user_id = request_data.get("user_id")
    playlist_name = request_data.get("playlist_name")
    playlist_description = request_data.get("playlist_description")
    playlist_tracks = request_data.get("playlist_tracks")

    if user_id is None:
      return {"error": "User ID is required"}, 400
    
    user = membership_services.get_user_by_id(user_id)
    if user is None:
      return {"error": "User not found"}, 404
    
    playlist =  music_services.create_playlist(
      name=playlist_name,
      description=playlist_description,
      user_id=user.id,
      api=True,
    )

    for track_id in playlist_tracks:
      music_services.create_playlist_item(
        playlist_id=playlist.id,
        track_id=track_id,
        user_id=user.id,
      )

    return {
      "action": "created",
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
  
  def delete(self, playlist_id):
    
    playlist = music_services.get_playlist_by_id(playlist_id)

    if playlist is None:
      return {"error": "Playlist not found"}, 404
    
    playlist_items = music_services.get_playlist_items_by_playlist_id(playlist_id)

    for playlist_item in playlist_items:
      music_services.delete_playlist_item(playlist_item.id)
    
    music_services.delete_playlist(playlist_id)
    return {
      "action": "deleted",
    }, 200


    