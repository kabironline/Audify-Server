from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, current_user
import music.services as services

class CommentAPIV2(Resource):
  def get(self, track_id):
    comments = services.get_comments_by_track_id(track_id)
    comment_dict = [services.get_comment_dict(comment) for comment in comments]
    return {
      "track_id": track_id,
      "comments": comment_dict,
      "action": "retrieved",
    }, 200
  @jwt_required()
  def post(self, track_id):
    request_data = request.get_json()
    comment = request_data.get("comment")
    user = current_user
    if comment is None:
      return {"error": "Comment is required"}, 400

    comment_object = services.create_comment(comment, track_id, user.id)    
    return {
      "comment": services.get_comment_dict(comment_object),
      "action": "created",
    }, 201

  @jwt_required()
  def delete(self, track_id, comment_id):
    if comment_id is None:
      return {"error": "Comment ID is required"}, 400

    comment = services.get_comment_by_id(comment_id)
    
    if comment is None:
      return {"error": "Comment does not exist"}, 400

    if comment.track_id != track_id:
      return {"error": "Comment does not belong to track"}, 400

    if comment.user_id != current_user.id:
      return {"error": "Unauthorized to delete comment"}, 401

    services.delete_comment(comment_id)

    return {
      "comment_id": comment_id,
      "action": "deleted",
    }, 200
