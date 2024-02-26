import os
from flask_restful import Resource, request
import membership.services as services
from werkzeug.datastructures import FileStorage

class ChannelAPI(Resource):
  def get(self, channel_id=None, channel=None):
    if channel_id is None and channel is None:
      return {"error": "channel_id or channel is required"}, 400
    if channel_id is not None:
      channel = services.get_channel_by_id(channel_id)
    elif channel is not None:
      channel = services.get_channel_by_name(channel)
    if channel is None:
      return {"error": "Channel not found"}, 404
    member = services.get_channel_members(channel.id)
    member_dict = [services.get_member_dict(m) for m in member]
    return {
      "channel": services.get_channel_dict(channel),
      "members": member_dict,
      "action": "retrieved",
    }, 200
  
  def post(self):
    request_data = request.get_json()
    name = request_data.get("name")
    bio = request_data.get("bio")
    password = request_data.get("password")
    user_id = request_data.get("user_id")

    # Checking if the user already has a channel or not
    user = services.get_user_by_id(user_id)

    if password is None:
      return {"error": "Password is required"}, 400
    
    if password != user.password:
      return {"error": "Invalid Password"}, 400

    if user is None:
      return {"error": "User not found"}, 404
    
    # Checking if the user already a member of a channel
    member = services.get_user_channels(user.id)
    
    if member is not None:
      return {"error": "User already has a channel"}, 400
    
    if name is None:
      return {"error": "Name of the Channel is Required"}, 400
    
    bio = "" if bio is None else bio

    name = name.strip()
    bio = bio.strip()

    services.create_channel(name=name, description=bio, api=True)

    channel = services.get_channel_by_name(name=name)

    # Registering the user as a member of the channel
    services.create_member(user.id, channel.id)

    # Avatar
    if "avatar" in request.files:
      avatar = request.files["avatar"]
      try:
        avatar.save(os.path.join("media", "avatars", f"{channel.id}.png"))
      except:
        services.delete_channel_by_id(channel.id)
        return {"error": "Error saving the avatar, Channel created successfully."}, 500

    return {"message": "Channel created successfully"}, 201

  def put(self, channel_id):
    request_data = request.get_json()
    name = request_data.get("name")
    bio = request_data.get("bio")
    password = request_data.get("password")

    if channel_id is None:
      return {"error": "channel_id is required"}, 400
    
    channel = services.get_channel_by_id(channel_id)
    if channel is None:
      return {"error": "Channel not found"}, 404
    
    if password != channel.password:
      return {"error": "Incorrect password"}, 400
    
    avatar = None

    if "avatar" in request.files:
      avatar = request.files["avatar"]
      

    services.update_channel(channel_id=channel_id, name=name, bio=bio, channel_art=avatar)
    return {"message": "Channel updated successfully"}, 200
  
  def delete(self, channel_id):
    request_data = request.get_json()
    password = request_data.get("password")

    if channel_id is None:
      return {"error": "channel_id is required"}, 400
    
    channel = services.get_channel_by_id(channel_id)
    if channel is None:
      return {"error": "Channel not found"}, 404
    
    if password != channel.password:
      return {"error": "Incorrect password"}, 400
    
    services.delete_channel_by_id(channel_id)
    return {"message": "Channel deleted successfully"}, 200