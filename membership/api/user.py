from flask_restful import Resource, request
from flask import jsonify, url_for
import membership.services as services
from werkzeug.datastructures import FileStorage
import os

class UserAPIV2(Resource):
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

    # popping the password for security reasons
    user_dict.pop("password")

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
  
  def put(self):
    request_data = request.get_json()
    user_id = request_data.get("user_id")
    nickname = request_data.get("nickname")
    bio = request_data.get("bio")
    password = request_data.get("password")

    if user_id is None:
      return {"error": "user_id is required"}, 400
    
    user = services.get_user_by_id(user_id)
    if user is None:
      return {"error": "User not found"}, 404
    
    # Updating user if the password is provided

    if password != user.password:
      return {"error": "Incorrect password"}, 400
    
    user.nickname = nickname or user.nickname
    user.bio = bio or user.bio
    user.password = password or user.password

    services.update_user(user)

    if "avatar" in request.files:
      avatar = request.files["avatar"]
      try:
        avatar.save(os.path.join("media", "avatars", f"{user.id}.png"))
      except:
        return {"error": "Error saving the avatar, user data updated"}, 500
    
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