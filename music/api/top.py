from flask_restful import Resource, request
from music.services import get_top_tracks,get_top_rated_tracks, get_track_dict, get_top_rated_channels, get_channel_dict, get_track_rating_for_user
from core.db import get_redis
import json
class TopAPI(Resource):
  def get(self):
    route = request.path.split("/")[3]
    count = request.args.get("n", 10)

    r = get_redis()
    r_top = r.get(f'top-{route}-{count}')
    r_top_counter= int(r.get(f'top-{route}-{count}-counter') or 0)
    if r_top and r_top_counter:
      if r_top_counter == 1:
        r.expire(f'top-{route}-{count}-counter', 1)
        r.expire(f'top-{route}-{count}', 1)
      r.set(f'top-{route}-{count}-counter', r_top_counter - 1)
      return json.loads(r_top), 200
    if route == "tracks":
      tracks = []
      mode = request.path.split("/")[5]
      if mode == "ratings":
        tracks = get_top_rated_tracks(count)
      elif mode == "views":
        tracks = get_top_tracks(count)
      top_json = [(get_track_dict(track)) for track in tracks]
    elif route == "channels":
      top = get_top_rated_channels(count)
      top_json = [(get_channel_dict(channel)) for channel in top]
    else:
      return {
        "error": "Invalid route"
      }, 400
    
    final_json = {
      "top": top_json,
    }
    r.set(f'top-{route}-{count}', json.dumps(final_json))
    r.set(f'top-{route}-{count}-counter', 10)
    r.expire(f'top-{route}-{count}', 600)
    r.expire(f'top-{route}-{count}-counter', 600)
    return final_json, 200