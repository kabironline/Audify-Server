import flask_restful import Resource, requests
import admin.services as services
import membership.services as membership_services
import music.services as music_services
from flask_jwt_extended import jwt_required, current_user

class AdminAPI (Resource):

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
        services.create_track_flag(track.id)
      elif action == "unflag":
        services.delete_track_flag(track.id)
    
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