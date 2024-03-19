from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, current_user
import music.services as music_services
import membership.services as membership_services

class SearchAPI(Resource):
  @jwt_required(optional=True)
  def get(self):
    query = request.args.get("q")
    if query is None:
      return {"error": "Query not found"}, 400
    
    user = None
    if request.headers.get("Authorization"):
      user = current_user


    genre = music_services.search_genres(query)
    if len(genre):
      return {
        "genre": music_services.get_genre_dict(genre[0])
      }

    tracks = music_services.search_tracks(query)
    albums = music_services.search_albums(query)
    channels = membership_services.search_channels(query)
    playlists = music_services.search_playlists(query)

    track_dicts = [music_services.get_track_dict(music_services.get_track_by_id(track.rowid)) for track in tracks]
    
    if user is not None:
      track_ratings = music_services.get_track_rating_for_user(user.id, *[track.rowid for track in tracks])
      for track in track_dicts:
        track["rating"] = track_ratings.get(track["id"], None)

    album_dicts = [music_services.get_album_dict(music_services.get_album_by_id(album.rowid)) for album in albums]
    channel_dicts = [membership_services.get_channel_dict(channel) for channel in channels]
    playlist_dicts = [music_services.get_playlist_dict(music_services.get_playlist_by_id(playlist.rowid)) for playlist in playlists]

    return {
      "tracks": track_dicts,
      "albums": album_dicts,
      "channels": channel_dicts,
      "playlists": playlist_dicts
    }, 200
    

