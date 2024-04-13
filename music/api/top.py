from flask_restful import Resource, request
from music.services import get_top_tracks,get_top_rated_tracks, get_track_dict, get_top_rated_channels
from membership.services import get_channel_dict
from core.db import get_redis
import json
class TopAPI(Resource):
  def get(self):
    route = request.path.split("/")[3]
    count = request.args.get("n", 10)

    r = get_redis()
    redis_path = f'top-{route}-{count}' if route != "tracks" else f'top-{request.path.split('/')[5]}-{route}-{count}'
    r_top = r.get(redis_path)
    r_top_counter= int(r.get(f'{redis_path}-counter') or 0)
    
    if r_top and r_top_counter:
      if r_top_counter == 1:
        r.delete(f'top-{route}-{count}-counter')
        r.delete(f'top-{route}-{count}')
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
      f"{route}": top_json,
    }
    r.set(f'top-{route}-{count}', json.dumps(final_json))
    r.set(f'top-{route}-{count}-counter', 10)
    r.expire(f'top-{route}-{count}', 600)
    r.expire(f'top-{route}-{count}-counter', 600)
    return final_json, 200