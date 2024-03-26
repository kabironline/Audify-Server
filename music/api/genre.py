from flask_restful import Resource, request
import music.services as services
from core.db import get_redis
import json
class GenreAPI(Resource):
  def get(self, genre_id=None):
    r = get_redis()
    tracks = "tracks" in request.path
    if tracks:
      if r.get(f"genre-{genre_id}-tracks"):
        return json.loads(r.get(f"genre-{genre_id}-tracks")), 200
      tracks = services.get_genre_tracks(genre_id)
      tracks_json = [services.get_track_dict(track) for track in tracks]
      final_json = {
        "tracks": tracks_json,
        "genre": services.get_genre_dict(services.get_genre_by_id(genre_id)),
      }
      r.set(f"genre-{genre_id}-tracks", json.dumps(final_json), ex=600)
      return final_json, 200
    else:
      if r.get("genres"):
        return json.loads(r.get("genres")), 200
      genres = services.get_all_genres()
      genres_json = [services.get_genre_dict(genre) for genre in genres]
      final_json = {
        "genres": genres_json,
      }
      r.set("genres", json.dumps(final_json), ex=600)
      return  final_json, 200