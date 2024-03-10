from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, current_user
import membership.services as services
from music.services import get_playlist_by_user, get_playlist_dict
from werkzeug.datastructures import FileStorage
import os

class UserAPIV2(Resource):
  @jwt_required(optional=True)
  def get(self, user_id: int = None, username: str = None):
    self_info = False
    if user_id is not None:
      user = services.get_user_by_id(user_id)
    elif username is not None:
      user = services.get_user_by_username(username=username)
    elif request.headers.get("Authorization") is not None:
      user = current_user
      self_info = True
    else:
      return {"error": "user_id or username is required"}, 400
    
    if user is None:
      return {"error": "User not found"}, 404
    
    user_dict = services.get_user_dict(user)
    
    if self_info:
      playlists = get_playlist_by_user(user.id)
      user_dict["playlists"] = [get_playlist_dict(playlist) for playlist in playlists]

      channels = services.get_user_channels(user.id)
      user_dict["channels"] = [services.get_channel_dict(services.get_channel_by_id(channel.id)) for channel in channels]

    return user_dict, 200
  
  def post(self):
    request_data = request.get_json()
    username = request_data.get("username")
    nickname = request_data.get("nickname") or username
    bio = request_data.get("bio")
    password = request_data.get("password")

    if username is None or password is None:
      return {"error": "Username and Password are required"}, 400
    
    # Checking if the user exists
    user = services.get_user_by_username(username=username)
    if user is not None:
      return {"error": "Username taken, try another one"}, 400
    
    # Creating user

    services.create_user(
      username=username, password=password, bio=bio, nickname=nickname
    )

    user = services.get_user_by_username(username=username)

    if "avatar" in request.files:
      avatar = request.files["avatar"]
      try:
        avatar.save(os.path.join("media", "avatars", f"{user.id}.png"))
      except:
        services.delete_user_by_id(user.id)
        return {"error": "Error saving the avatar"}, 500
    
    return {"message": "User created successfully"}, 201
  
  @jwt_required()
  def put(self):
    request_data = request.form
    nickname = request_data.get("nickname")
    bio = request_data.get("bio")
    password = request_data.get("password")
    new_password = request_data.get("new_password")
    
    user = current_user

    if user is None:
      return {"error": "User not found"}, 404
    
    if password != user.password:
      return {"error": "Incorrect password"}, 400
    

    user.nickname = nickname or user.nickname
    user.bio = bio or user.bio
    user.password = new_password or user.password
    
    if "avatar" in request.files:
      user.avatar = request.files["avatar"]

    services.update_user(user)

    return {"message": "User updated successfully"}, 200
  
  def delete(self):
    request_data = request.get_json()
    user_id = request_data.get("user_id")

    if user_id is None:
      return {"error": "user_id is required"}, 400
    
    user = services.get_user_by_id(user_id)
    if user is None:
      return {"error": "User not found"}, 404
    
    services.deactivate_user(user)

    return {"message": "User deleted successfully"}, 200