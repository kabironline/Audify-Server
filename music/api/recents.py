from flask_restful import Resource, request
from music.services import get_recent_by_user_id, get_track_dict, create_recent, create_new_view, get_track_by_id
from membership.services import get_user_by_id
from flask_jwt_extended import jwt_required, current_user

class RecentsAPI(Resource):

  @jwt_required()
  def get(self, user_id=None):
    user_id = current_user.id if user_id is None else user_id
    if user_id == None:
      return {"error": "User ID is required"}, 400
    
    user = get_user_by_id(user_id)
    if user is None:
      return {"error": "User not found"}, 404
    
    n = request.args.get("n", 10)
    recents = get_recent_by_user_id(user_id, n)
    recents_json = [(get_track_dict(recent)) for recent in recents]
    return {
      "recents": recents_json,
    }, 200
  
  @jwt_required()
  def post(self):
    request_data = request.get_json()
    track_id = request_data.get("track_id")
    user_id = current_user.id

    if track_id is None:
      return {"error": "Track ID is required"}, 400
    
    track = get_track_by_id(track_id)
    if track is None:
      return {"error": "Track not found"}, 404
    
    create_recent(user_id, track_id)
    create_new_view(track, user_id)
    return {
      "action": "updated",
    }, 201
  