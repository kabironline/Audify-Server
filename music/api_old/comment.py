from flask_restful import Resource, request
import music.services as services
import core
from flask_cors import cross_origin


class CommentAPI(Resource):
    @cross_origin()
    def get(self, track_id):
        comments = services.get_comments_by_track_id(track_id)
        comment_dict = [services.get_comment_dict(comment) for comment in comments]
        return {
            "track_id": track_id,
            "comments": comment_dict,
            "action": "retrieved",
        }, 200

    @cross_origin()
    def post(self, track_id) -> [dict, int]:
        # Reading the rating from the request body
        request_data = request.get_json()
        comment = request_data.get("comment")
        user_id = request_data.get("user_id")
        if comment is None:
            return {"error": "Comment is required"}, 400

        comment_object = services.create_comment(comment, track_id, user_id)

        if comment_object is None:
            return {
                "track_id": track_id,
                "user_id": user_id,
                "action": "deleted",
            }, 200

        return {
            "comment": services.get_comment_dict(comment_object),
            "action": "created",
        }, 201

    @cross_origin()
    def delete(self, track_id, comment_id):
        if comment_id is None:
            return {"error": "Comment ID is required"}, 400

        comment = services.get_comment_by_id(comment_id)

        if comment is None:
            return {"error": "Comment does not exist"}, 400

        services.delete_comment(comment_id)

        return {
            "track_id": track_id,
            "comment_id": comment_id,
            "action": "deleted",
        }, 200
