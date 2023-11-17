from flask_restful import Resource, request
import music.services as services
import core
from flask_cors import cross_origin


class RatingAPI(Resource):
    @cross_origin()
    def get(self, track_id):
        rating = services.get_track_rating(track_id)
        return {
            "track_id": track_id,
            "rating": rating,
            "action": "retrieved",
        }, 200

    @cross_origin()
    def post(self, track_id) -> [dict, int]:
        user_id = core.current_user.id

        # Reading the rating from the request body
        request_data = request.get_json()
        rating = request_data.get("rating")

        if rating is None:
            return {"error": "Rating is required"}, 400

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

    @cross_origin()
    def delete(self, track_id):
        user_id = core.current_user.id
        services.delete_rating(track_id, user_id)
        return {"track_id": track_id, "user_id": user_id, "action": "deleted"}, 200

    @cross_origin()
    def put(self, track_id):
        user_id = core.current_user.id

        # Read the rating from the request body
        request_data = request.get_json()
        rating = request_data.get("rating")

        if rating is None:
            return {"error": "Rating is required"}, 400

        services.create_or_update_rating(track_id, user_id, rating)
        return {
            "track_id": track_id,
            "user_id": user_id,
            "rating": rating,
            "action": "updated",
        }, 201

    @cross_origin()
    def options(self):
        return {}, 200
