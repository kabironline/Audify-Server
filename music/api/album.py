from flask_restful import Resource, request
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
import music.services as music_services
import membership.services as membership_services
from werkzeug.datastructures import FileStorage
from datetime import datetime

class AlbumAPI(Resource):
  @jwt_required(optional=True)
  def get(self, album_id):
    album = music_services.get_album_by_id(album_id)
    if album is None:
      return {"error": "Album not found"}, 404
    
    album_items = music_services.get_album_tracks_by_album_id(album_id)
    ratings = {}    
    
    auth_header = request.headers.get("Authorization")
    if auth_header != '':
      user_id = get_jwt_identity()
      user = membership_services.get_user_by_id(user_id)
      ratings = music_services.get_track_rating_for_user(user.id, *[album_item.id for album_item in album_items])
    for track in album_items:
      track.rating = ratings.get(track.id, None)
    tracks = [music_services.get_track_dict(album_item) for album_item in album_items]
    album_dict = music_services.get_album_dict(album)
    album_dict["tracks"] = tracks
    return {
      "album": album_dict
    }, 200
  
  @jwt_required()
  def post(self):
    request_data = request.form
    album_name = request_data.get("album_name")
    album_description = request_data.get("album_description")
    album_art = request.files.get("album_art")
    release_date = request_data.get("release_date")
    creator = current_user.channel
    
    release_date = datetime.strptime(release_date, "%Y-%m-%d")

    album = music_services.create_album(
      name=album_name,
      description=album_description,
      release_date=release_date,
      album_art=album_art,
      channel_id=creator.id,
    )
    if "album_tracks" in request_data:
      album_tracks = request_data.get("album_tracks")
      if type(album_tracks) == str: album_tracks = [album_tracks]
      for track_id in album_tracks:
        track_id = int(track_id)
        music_services.create_album_item(
          album_id=album.id,
          track_id=track_id,
          user_id=creator.id,
        )

    return {"action": "created"}, 201
  
  def put(self, album_id):
    request_data = request.get_json()
    album_name = request_data.get("album_name")
    album_tracks = request_data.get("album_tracks")
    album_art = request_data.get("album_art")
    release_date = request_data.get("release_date")
    creator_name = request_data.get("creator_name")

    if creator_name is None:
      return {"error": "creator_name is required"}, 400
    
    creator = membership_services.get_channel_by_name(creator_name)
    if creator is None:
      return {"error": "creator not found"}, 404
    
    release_date = datetime.strptime(release_date, "%Y-%m-%d")
    
    album_art_file = open(album_art, "rb")
    album_art = FileStorage(album_art_file)
    album_art_file.close()

    album = music_services.update_album(
      album_id=album_id,
      name=album_name,
      release_date=release_date,
      album_art=album_art,
      channel_id=creator.id,
    )

    for track_id in album_tracks:
      music_services.create_album_item(
        album_id=album.id,
        track_id=track_id,
      )

    return {"action": "updated"}, 200
  
  @jwt_required()
  def delete(self, album_id):
    import pdb; pdb.set_trace()
    album = music_services.get_album_by_id(album_id)
    
    if album is None:
      return {"error": "Album not found"}, 404
    

    album_items = music_services.get_album_items_by_album_id(album_id)

    if album.created_by != current_user.channel.id:
      return {"error": "Unauthorized"}, 401

    for album_item in album_items:
      music_services.delete_album_item(album_item.id)

    music_services.delete_album(album_id, current_user.channel.id, True)

    return {"action": "deleted"}, 200

