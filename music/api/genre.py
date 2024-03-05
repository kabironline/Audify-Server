from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, current_user
import music.services as services

class GenreAPI(Resource):
  @jwt_required(optional=True)
  def get(self, genre_id=None):
    tracks = "tracks" in request.path
    if tracks:
      tracks = services.get_genre_tracks(genre_id)
      if request.headers.get("Authorization"):
        ratings = services.get_track_rating_for_user(current_user.id, *[track.id for track in tracks])
        for track in tracks:
          track.rating = ratings.get(track.id, None)

      tracks_json = [services.get_track_dict(track) for track in tracks]
      return {
        "tracks": tracks_json,
      }, 200
    else:
      # returning the all genres list
      genres = services.get_all_genres()
      genres_json = [services.get_genre_dict(genre) for genre in genres]

      return {
        "genres": genres_json,
      }, 200