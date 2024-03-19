from flask_restful import Resource, request
from flask import jsonify, url_for
import membership.services as services
from flask_cors import cross_origin
from werkzeug.datastructures import FileStorage
import os


class UserAPI(Resource):
    @cross_origin()
    def get(self, user_id: int = None, username: str = None):
        if user_id is None and username is None:
            return {"error": "user_id or username is required"}, 400
        if user_id is not None:
            user = services.get_user_by_id(user_id)
        elif username is not None:
            user = services.get_user_by_username(username=username)

        if user is None:
            return {"error": "User not found"}, 404

        user_dict = services.get_user_dict(
            user, avatar=url_for("user_avatar", user_id=user_id)
        )

        return user_dict, 200

    def post(self) -> [dict, int]:
        request_data = request.get_json()
        username = request_data.get("username")
        nickname = request_data.get("nickname") or username
        bio = request_data.get("bio")
        password = request_data.get("password")

        if username is None or password is None:
            return {"error": "username and password are required"}, 400


        # Checking if the user exists
        user = services.get_user_by_username(username=username)
        if user is not None:
            return {"error": "username taken, try another one"}, 400

        # Everything is good. Create the user
        services.create_user(
            username=username, password=password, bio=bio, nickname=nickname
        )

        user = services.get_user_by_username(username=username)

        # Check if the request has an avatar
        if "avatar" in request.files:
            avatar = request.files["avatar"]
            return {"message": "User created successfully"}, 201

        elif request_data.get("avatar") is not None:
            # Get the png file from the path provided
            avatar = request_data.get("avatar")
            avatar_file = open(avatar, "rb")
            avatar = FileStorage(avatar_file)
        else:
            return {"message": "User created successfully"}, 201

        os.mkdir(f"media/users/{user.id}")
        avatar.save(f"media/users/{user.id}/avatar.png")

        return {"message": "User created successfully"}, 201

    def put(self, user_id):
        user = services.get_user_by_id(user_id)

        if user is None:
            return {"error": "User not found"}, 404

        request_data = request.get_json()
        username = request_data.get("nickname")
        bio = request_data.get("bio")
        password = request_data.get("password")

        if username is None and bio is None and password is None:
            return {"error": "No data to update"}, 400

        user.username = username if username else user.username
        user.bio = bio if bio else user.bio
        user.password = password if password else user.password

        if "avatar" in request.files:
            user.avatar = request.files["avatar"]

        services.update_user(user)

        return {"message": "User updated successfully"}, 200

    def delete(self, user_id):
        user = services.get_user_by_id(user_id)

        if user is None:
            return {"error": "User not found"}, 404

        services.delete_user_by_id(user_id)
