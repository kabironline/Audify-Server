from flask_restful import Resource, request
import music.services as services

class LatestAPI(Resource):
  def get(self):
    latest = services.get_latest_tracks()
    latest_json = [(services.get_track_dict(track)) for track in latest]
    return {
      "latest": latest_json,
    }, 200