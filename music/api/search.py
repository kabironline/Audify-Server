from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, current_user
import music.services as music_services
import membership.services as membership_services

class SearchAPI(Resource):
  def get(self):
    query = request.args.get("q")
    if query is None:
      return {"error": "Query not found"}, 400
    
    genre = music_services.search_genres(query)
    if len(genre):
      return {
        "genre": music_services.get_genre_dict(genre[0])
      }

    tracks = music_services.search_tracks(query)
    albums = music_services.search_albums(query)
    channels = membership_services.search_channels(query)
    playlists = music_services.search_playlists(query)

    track_dicts = [music_services.get_track_by_id(track.rowid) for track in tracks]
    # removing flagged tracks or tracks from blacklisted channels
    track_dicts = [music_services.get_track_dict(track) for track in track_dicts if not track.flagged and not track.channel.blacklisted]
    
    album_dicts = [(music_services.get_album_by_id(album.rowid)) for album in albums]
    album_dicts = [music_services.get_album_dict(album) for album in album_dicts if not album.channel.blacklisted]
    
    channel_dicts = [(channel) for channel in channels]
    channel_dicts = [membership_services.get_channel_dict(channel) for channel in channel_dicts if not channel.blacklisted]
    
    playlist_dicts = [music_services.get_playlist_dict(music_services.get_playlist_by_id(playlist.rowid)) for playlist in playlists]

    return {
      "tracks": track_dicts,
      "albums": album_dicts,
      "channels": channel_dicts,
      "playlists": playlist_dicts
    }, 200
    

