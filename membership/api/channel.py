import os
from flask_restful import Resource, request
import membership.services as services
from music.services import get_album_dict, get_track_dict, get_tracks_by_channel, get_album_by_user, get_track_rating_for_user, get_channel_track_count, get_channel_album_count, get_views_by_channel_id
from flask_jwt_extended import jwt_required, current_user
from admin.services import get_whitelist_by_channel_id
from core.db import get_redis
import json

class ChannelAPIV2(Resource):
  def get(self, channel_id):
    r = get_redis()
    channel_dict = None
    channel = None
    
    if r.get(f"channel:{channel_id}") is not None:
      channel_dict = json.loads(r.get(f"channel:{channel_id}"))
    else:
      channel = services.get_channel_by_id(channel_id)
      if channel is None:
        return {"error": "Channel not found"}, 404
      member = services.get_channel_members(channel.id)
      member_dict = [services.get_member_dict(m) for m in member]
      is_whitelisted = True if get_whitelist_by_channel_id(channel.id) is not None else False
      channel.whitelisted = is_whitelisted
      channel_dict = {
        "channel": services.get_channel_dict(channel),
        "members": member_dict,
        "action": "retrieved",
      }
      r.set(f"channel:{channel_id}", json.dumps(channel_dict), ex=3600)
    
    detail_level = request.args.get("detail") or "default"
    if detail_level == "full":
      # get all the tracks and albums of the channel
      albums = get_album_by_user(channel_id, count=6)
      album_dict = [get_album_dict(a) for a in albums]
      channel_dict["albums"] = album_dict
      channel_dict["tracks"] = get_channel_tracks(channel_id, 6)
      # append the tracks and albums to the channel_dict
      track_info = get_channel_track_count(channel_id)
      album_info = get_channel_album_count(channel_id)
      views = get_views_by_channel_id(channel_id)
      info = {
        "tracks": track_info,
        "albums": album_info,
        "views": views
      }
      channel_dict["info"] = info
      return channel_dict, 200
    elif detail_level == "tracks":
      channel_dict["tracks"] = get_channel_tracks(channel_id, 30)
      return channel_dict, 200
    elif detail_level == "albums":
      albums = get_album_by_user(channel_id, count=6)
      album_dict = [get_album_dict(a) for a in albums]
      channel_dict["albums"] = album_dict
      return channel_dict, 200
    elif detail_level == "all_tracks":
      channel_dict["tracks"] = get_channel_tracks(channel_id,10000)
      return channel_dict, 200
    elif detail_level == "default":
      return channel_dict, 200
    else:
      return {"error": "Invalid detail level"}, 400


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
    
    r = get_redis()
    r.delete(f"channel:{channel.id}")

    return {"message": "Channel updated successfully"}, 200
  
  @jwt_required()  
  def delete(self):
    
    members = services.get_user_channels(current_user.id)
    if members is None:
      return {"error": "User is not a member of any channel"}, 404
    r = get_redis()
    for member in members:
      services.deactivate_channel(member.channel_id)
      r.delete(f"channel:{member.channel_id}")

    return {"message": "Channel deleted successfully"}, 200
  
def get_channel_tracks(channel_id, count=30, user_id=None):
  tracks = get_tracks_by_channel(channel_id, count=count)
  if user_id is not None:
    ratings = get_track_rating_for_user(user_id, *[t.id for t in tracks])
    for track in tracks:
      track.rating = ratings.get(track.id, None)
  return [get_track_dict(t) for t in tracks]
