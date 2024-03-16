from flask_restful import Resource, request
import admin.services as services
import membership.services as membership_services
import music.services as music_services
from flask_jwt_extended import jwt_required, current_user

class AdminAPI (Resource):

  @jwt_required()
  def get(self):
    # fetching all the data for the admin dashboard
    admin_user = current_user
    if not admin_user.is_admin:
      return {"error": "You are not an admin"}, 403

    last = request.path.split("/")[-1]
    if last == "data":
      tracks = len(music_services.get_all_tracks())
      genres = len(music_services.get_all_genres())
      albums = len(music_services.get_all_albums())
      playlists = len(music_services.get_all_playlists())
      users = len(membership_services.get_all_users())
      channels = len(membership_services.get_all_channels())
      blacklisted_channels = len(services.get_blacklist())
      whitelisted_channels = len(services.get_whitelist())

      return {
        "tracks": tracks,
        "genres": genres,
        "albums": albums,
        "playlists": playlists,
        "users": users,
        "channels": channels,
        "blacklisted_channels": blacklisted_channels,
        "whitelisted_channels": whitelisted_channels
      }, 200
    
    elif last == "graphs":
      genre_distribution_graph = services.generate_genre_distribution_graph(True)
      user_channel_distribution_graph = services.generate_user_channel_distribution_graph(True)
      genre_listener_graph = services.generate_genre_listener_graph(True)
      viewership_graph = services.generate_recent_viewership_graph(True)

      return {
        "genre_distribution_graph": genre_distribution_graph,
        "user_channel_distribution_graph": user_channel_distribution_graph,
        "genre_listener_graph": genre_listener_graph,
        "viewership_graph": viewership_graph
      }, 200
    
    elif last == "tracks":
      tracks = music_services.get_all_tracks()      
      return {"tracks": [music_services.get_track_dict(track) for track in tracks]}, 200


  @jwt_required()
  def post(self, action=None, id=None, type=None):

    admin_user = current_user
    if not admin_user.is_admin:
      return {"error": "You are not an admin"}, 403
    
    if action is None:
      return {"error": "Action is required"}, 400
    elif id is None:
      return {"error": "ID is required"}, 400
    elif type is None:
      return {"error": "Type is required"}, 400
    
    if type not in ["track", "channel"]:
      return {"error": "Invalid type"}, 400
    

    if type == "channel":
      if action not in ["blacklist", "whitelist"]:
        return {"error": "Invalid action"}, 400
      channel = membership_services.get_channel_by_id(id)
      if channel is None:
        return {"error": "Channel not found"}, 404
      if action == "blacklist":
        if services.get_whitelist_by_channel_id(channel.id):
          return {"error": "Channel is whitelisted"}, 400
        services.blacklist_channel(channel.id)
      elif action == "whitelist":
        if channel.blacklisted:
          return {"error": "Channel is blacklisted"}, 400
        services.whitelist_channel(channel.id)
    
    elif type == "track":
      if action not in ["flag", "unflag"]:
        return {"error": "Invalid action"}, 400
      track = music_services.get_track_by_id(id)
      if track is None:
        return {"error": "Track not found"}, 404
      
      if action == "flag":
        services.create_track_flag(track.id, admin_user.id)
      elif action == "unflag":
        services.delete_track_flag(track.id, admin_user.id)
    
    else:
      return {"error": "Invalid type"}, 400
    
    return {"message": "Success"}, 200
      
  @jwt_required()
  def delete(self, action=None, id=None, type=None):
    
    admin_user = current_user
    if not admin_user.is_admin:
      return {"error": "You are not an admin"}, 403
    
    if action is None:
      return {"error": "Action is required"}, 400
    elif id is None:
      return {"error": "ID is required"}, 400
    elif type is None:
      return {"error": "Type is required"}, 400
    
    if type not in ["track", "channel"]:
      return {"error": "Invalid type"}, 400
    
    if type == "channel":
      if action not in ["blacklist", "whitelist"]:
        return {"error": "Invalid action"}, 400
      channel = membership_services.get_channel_by_id(id)
      if channel is None:
        return {"error": "Channel not found"}, 404
      if action == "blacklist":
        services.delete_blacklist(channel.id, admin_user.id)
      elif action == "whitelist":
        services.delete_whitelist_by_channel_id(channel.id)
      else:
        return {"error": "Invalid action"}, 400
      
    elif type == "track":
      if action not in ["flag", "unflag"]:
        return {"error": "Invalid action"}, 400
      track = music_services.get_track_by_id(id)
      if track is None:
        return {"error": "Track not found"}, 404
      if action == "flag" or action == "unflag":
        services.delete_track_flag(track.id)