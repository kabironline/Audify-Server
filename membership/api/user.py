from flask_restful import Resource, request
import membership.services as services
import core
from flask_cors import cross_origin


class UserAvatarAPI(Resource):
    @cross_origin()
    def get(user_id):
        avatar = services.get_user_avatar(user_id)

        if avatar is None:
            return "", 404

        return {
            "user_id": user_id,
            "avatar": avatar,
            "action": "retrieved",
        }, 200

    def post(user_id) -> [dict, int]:
        user_id = core.current_user.id

        # Reading the avatar from the request body
        request_data = request.get_json()
        avatar = request_data.get("avatar")

        if avatar is None:
            return {"error": "Avatar is required"}, 400

        avatar_object = services.create_or_update_avatar(user_id, avatar)

        if avatar_object is None:
            return {
                "user_id": user_id,
                "action": "deleted",
            }, 200

        return {
            "user_id": avatar_object.user_id,
            "avatar": avatar_object.avatar,
            "action": "created",
        }, 201
