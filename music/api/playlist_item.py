from flask_restful import Resource, request
import music.services as music_services
from flask_jwt_extended import jwt_required, current_user

class PlaylistItemAPI(Resource):
  @jwt_required()
  def post(self, playlist_id, track_id):
    user = current_user

    music_services.create_playlist_item(
      track_id=track_id,
      playlist_id=playlist_id,
      user_id=user.id,
    )

    return {
      "action": "added",
    }, 201

  @jwt_required()
  def delete(self, playlist_id, track_id):
    user = current_user

    playlist = music_services.get_playlist_by_id(playlist_id)
    if playlist.user.id != user.id:
      return {
        "error": "You are not authorized to remove this track from the playlist",
      }, 403


    music_services.delete_playlist_item_by_playlist_track_id(
      track_id=track_id,
      playlist_id=playlist_id,
    )

    return {
      "action": "removed",
    }, 200