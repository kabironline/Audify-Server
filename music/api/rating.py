from flask_restful import Resource, request
import music.services as services
import core


# TODO: Convert this to use JWT for authentication and identification
class RatingAPI(Resource):
  def get(self, track_id):
    rating = services.get_track_rating(track_id)
    return {
      "track_id": track_id,
      "rating": rating,
    }, 200
  
  def post(self, track_id):
    request_data = request.get_json()
    rating = request_data.get("rating")
    user_id = request_data.get("user_id")

    if rating is None:
      return {"error": "Rating is required"}, 400
    
    if user_id is None:
      return {"error": "User ID is required"}, 400
    
    rating_object = services.create_or_update_rating(track_id, user_id, rating)

    if rating_object is None:
      return {
        "track_id": track_id,
        "user_id": user_id,
        "action": "deleted",
      }, 200
    
    return {
      "track_id": rating_object.track_id,
      "user_id": rating_object.user_id,
      "rating": rating_object.rating,
      "action": "created",
    }, 201
  
  def put(self, track_id):
    request_data = request.get_json()
    rating = request_data.get("rating")
    user_id = core.current_user.id

    if rating is None:
      return {"error": "Rating is required"}, 400
    
    services.create_or_update_rating(track_id, user_id, rating)
    return {
      "track_id": track_id,
      "user_id": user_id,
      "rating": rating,
      "action": "updated",
    }, 200
  
  def delete(self, track_id):
    user_id = core.current_user.id
    services.delete_rating(track_id, user_id)
    return {"track_id": track_id, "user_id": user_id, "action": "deleted"}, 200
  
