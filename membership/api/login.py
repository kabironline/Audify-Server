from flask_restful import Resource, request
from flask import jsonify
import membership.services as membership_services
import music.services as music_services
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin

class LoginAPI(Resource):
  @cross_origin()
  def post(self):
    request_data = request.get_json()
    username = request_data.get("username")
    password = request_data.get("password")
    
    if username is None or password is None:
      return {"error": "Username and password are required"}, 400
    
    user = membership_services.get_user_by_username(username)
    if user is None:
      return {"error": "User not found"}, 404
    
    if user.password != password:
      return {"error": "Invalid password"}, 400
    
    access_token = create_access_token(identity=user.id)

    user_dict = membership_services.get_user_dict(user)

    # getting the user's playlists
    playlists = music_services.get_playlist_by_user(user.id)
    user_dict["playlists"] = []
    for playlist in playlists:
      playlist_dict = music_services.get_playlist_dict(playlist)
      user_dict["playlists"].append(playlist_dict)

    return jsonify(access_token=access_token, user=user_dict), 200