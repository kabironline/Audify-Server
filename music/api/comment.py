from flask_restful import Resource, request
import music.services as services
import core
from flask_cors import cross_origin


class CommentAPI(Resource):
    @cross_origin()
    def get(self, track_id):
        comments = services.get_comments_by_track_id(track_id)
        return {
            "track_id": track_id,
            "comments": comments,
            "action": "retrieved",
        }, 200

    @cross_origin()
    def post(self, track_id) -> [dict, int]:
        user_id = core.current_user.id

        # Reading the rating from the request body
        request_data = request.get_json()
        comment = request_data.get("comment")

        if comment is None:
            return {"error": "Comment is required"}, 400

        comment_object = services.create_comment(track_id, user_id, comment)

        if comment_object is None:
            return {
                "track_id": track_id,
                "user_id": user_id,
                "action": "deleted",
            }, 200

        return {
            "track_id": comment_object.track_id,
            "user_id": comment_object.user_id,
            "comment": comment_object.comment,
            "action": "created",
        }, 201
