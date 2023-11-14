from .db import *
from .utils import *
from membership.models import User
from flask import session

current_user = None

api = None


def set_api(api_instance):
    global api
    api = api_instance


def get_api():
    return api


def set_current_user(user: User):
    # Convert the user to a dictionary
    user_dict = {
        "id": user.id,
        "username": user.username,
        # "is_creator": user.is_creator,
        "is_admin": user.is_admin,
        "nickname": user.nickname,
        "bio": user.bio,
        "last_modified_by": user.last_modified_by,
        "created_by": user.created_by,
        "created_at": user.created_at,
        "last_modified_at": user.last_modified_at,
    }

    session["user"] = user_dict


def get_current_user() -> User:
    return session.get("user", None)
