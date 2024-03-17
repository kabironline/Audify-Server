import os
from flask_restful import Resource, request
import membership.services as services
from music.services import get_album_dict, get_track_dict, get_tracks_by_channel, get_album_by_user, get_track_rating_for_user
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from admin.services import get_whitelist_by_channel_id

class ChannelAPIV2(Resource):
  @jwt_required(optional=True)
  def get(self, channel_id=None):
    
    if channel_id is None:
      return {"error": "channel_id is required"}, 400
    if channel_id is not None:
      channel = services.get_channel_by_id(channel_id)
    if channel is None:
      return {"error": "Channel not found"}, 404
    
    
    user_id = None
    if request.headers.get("Authorization"):
      user_id = get_jwt_identity()

    if user_id is not None:
      user = current_user
      if user.is_admin:
        whitelist = get_whitelist_by_channel_id(channel.id)
        channel.whitelisted = True if whitelist is not None else False

    member = services.get_channel_members(channel.id)
    member_dict = [services.get_member_dict(m) for m in member]
    
    detail_level = request.args.get("detail")
    if detail_level == "full":
      # get all the tracks and albums of the channel
      albums = get_album_by_user(channel.id, count=6)
      album_dict = [get_album_dict(a) for a in albums]
      return {
        "channel": services.get_channel_dict(channel),
        "members": member_dict,
        "tracks": get_channel_tracks(channel.id, 6, user_id),
        "albums": album_dict,
        "action": "retrieved",
      }, 200
    
    elif detail_level == "tracks":
      return {
        "channel": services.get_channel_dict(channel),
        "members": member_dict,
        "tracks": get_channel_tracks(channel.id, 30, user_id),
        "action": "retrieved",
      }, 200
    
    elif detail_level == "albums":
      albums = get_album_by_user(channel.id, count=6)
      album_dict = [get_album_dict(a) for a in albums]
      return {
        "channel": services.get_channel_dict(channel),
        "members": member_dict,
        "albums": album_dict,
        "action": "retrieved",
      }, 200
    
    else:

      return {
        "channel": services.get_channel_dict(channel),
        "members": member_dict,
        "action": "retrieved",
      }, 200
  @jwt_required()  
  def post(self):
    request_data = request.form
    name = request_data.get("name")
    bio = request_data.get("bio")
    password = request_data.get("password")
    user = current_user

    if password is None:
      return {"error": "Password is required"}, 400
    
    if password != user.password:
      return {"error": "Invalid Password"}, 400


    if user is None:
      return {"error": "User not found"}, 404
    
    # Checking if the user already a member of a channel
    # member = services.get_user_channels(user.id)
    
    # if member is not None:
    #   return {"error": "User already has a channel"}, 400
    
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
        os.makedirs(os.path.join("media", "channels", f"{channel.id}"))
        avatar.save(os.path.join("media", "channels",f"{channel.id}", "avatar.png"))
      except Exception as e:
        print(e)
        return {"error": "Error saving the avatar, Channel created successfully."}, 500

    return {"message": "Channel created successfully"}, 201
  @jwt_required()
  def put(self):
    request_data = request.form
    name = request_data.get("name")
    bio = request_data.get("bio")
    password = request_data.get("password")
    channel = current_user.channel

    if password != current_user.password:
      return {"error": "Incorrect password"}, 400
    
    avatar = None

    if "avatar" in request.files:
      avatar = request.files["avatar"]

    services.update_channel(channel_id=channel.id, name=name, description=bio, channel_art=avatar)
    return {"message": "Channel updated successfully"}, 200
  
  @jwt_required()  
  def delete(self):
    
    members = services.get_user_channels(current_user.id)
    if members is None:
      return {"error": "User is not a member of any channel"}, 404
    
    for member in members:
      services.deactivate_channel(member.channel_id)

    return {"message": "Channel deleted successfully"}, 200
  
def get_channel_tracks(channel_id, count=30, user_id=None):
  tracks = get_tracks_by_channel(channel_id, count=count)
  if user_id is not None:
    ratings = get_track_rating_for_user(user_id, *[t.id for t in tracks])
    for track in tracks:
      track.rating = ratings.get(track.id, None)
  return [get_track_dict(t) for t in tracks]