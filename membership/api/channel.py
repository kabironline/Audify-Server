import os
from flask_restful import Resource, request
from flask import send_file
import membership.services as services
from flask_cors import cross_origin
from werkzeug.datastructures import FileStorage


class ChannelAPI(Resource):
    @cross_origin()
    def get(self, channel_id=None, channel_name=None):
        if channel_id is None and channel_name is None:
            # from the request get the ".../channel?name=..." or ".../channel?id=..."
            channel_id = request.args.get("id")
            channel_name = request.args.get("name")

            if channel_id is None and channel_name is None:
                return {"error": "Channel id or name not provided"}, 400
        channel = None

        if channel_id is None:
            channel = services.get_channel_by_name(channel_name)
        elif channel_name is None:
            channel = services.get_channel_by_id(channel_id)

        if channel is None:
            return {"error": "Channel not found"}, 404
        member = services.get_channel_members(channel.id)

        member_dict = [services.get_member_dict(m) for m in member]

        return {
            "channel": services.get_channel_dict(channel),
            "members": member_dict,
            "action": "retrieved",
        }, 200

    @cross_origin()
    def post(self) -> [dict, int]:
        request_data = request.get_json()
        name = request_data.get("name")
        bio = request_data.get("bio")
        password = request_data.get("password")

        bio = "" if bio is None else bio

        if name is None:
            return {"error": "Name of the Channel is Required"}, 400

        user = services.get_user_by_username(username=name)
        if user is None:
            services.create_user(name, password, name, bio)
            user = services.get_user_by_username(username=name)

        services.create_channel(name=name, description=bio, api=True)
        channel = services.get_channel_by_name(name=name)
        services.create_member(user.id, channel.id)

        avatar = request_data.get("avatar")
        avatar_file = open(avatar, "rb")
        avatar = FileStorage(avatar_file)

        try:
            os.mkdir(f"media/channels/{channel.id}")
            os.mkdir(f"media/users/{user.id}")
            avatar.save(f"media/users/{user.id}/avatar.png")
            # copy image from user to channel
            os.system(
                f"cp media/users/{user.id}/avatar.png media/channels/{channel.id}/avatar.png"
            )
        except:
            services.delete_channel_by_id(channel.id)
            services.delete_user_by_id(user.id)
            services.delete_channel_members(channel.id)
            return {"error": "Error creating channel"}, 500

        return {"message": "User created successfully"}, 201

    @cross_origin()
    def put(self, channel_id):
        channel = services.get_channel_by_id(channel_id)

        if channel is None:
            return {"error": "User not found"}, 404

        request_data = request.get_json()
        username = request_data.get("name")
        bio = request_data.get("desc")

        if username is None and bio is None:
            return {"error": "No data to update"}, 400

        channel = services.update_channel(channel_id, username=username, bio=bio)

        avatar = None
        if "avatar" in request.files:
            avatar = request.files["avatar"]
        elif request_data.get("avatar") is not None:
            with open(request_data.get("avatar"), "rb") as avatar_file:
                avatar = FileStorage(avatar_file)

        services.update_channel(channel_id, avatar=avatar)

        return {"message": "User updated successfully"}, 200

    @cross_origin()
    def delete(self, channel_id):
        user = services.get_user_by_id(channel_id)

        if user is None:
            return {"error": "User not found"}, 404

        services.delete_channel_by_id(channel_id)
