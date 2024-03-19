from membership.models import User
from flask import session

current_user = None

api = None


def set_api(api_instance):
    global api
    api = api_instance


def get_api():
    return api


def set_current_user(user: User, channel=None, playlist=[]):
    # Convert the user to a dictionary
    user_dict = {
        "id": user.id,
        "username": user.username,
        # "is_creator": user.is_creator,
        "is_admin": user.is_admin,
        "nickname": user.nickname,
        "bio": user.bio,
        "password": user.password,
        "last_modified_by": user.last_modified_by,
        "created_by": user.created_by,
        "created_at": user.created_at,
        "last_modified_at": user.last_modified_at,
        "channels": channel,
        "playlists": playlist,
    }

    session["user"] = user_dict
    session.permanent = True
    print(session["user"])


def logout():
    session.pop("user", None)


def get_current_user() -> User | None:
    user_dict = session.get("user")

    if user_dict is None:
        return None
    # Convert the user dict to a User object
    user = User(
        id=user_dict["id"],
        username=user_dict["username"],
        # is_creator=user_dict["is_creator"],
        is_admin=user_dict["is_admin"],
        nickname=user_dict["nickname"],
        bio=user_dict["bio"],
        password=user_dict["password"],
        last_modified_by=user_dict["last_modified_by"],
        created_by=user_dict["created_by"],
        created_at=user_dict["created_at"],
        last_modified_at=user_dict["last_modified_at"],
    )

    user.channels = user_dict["channels"]
    if "playlists" in user_dict:
        user.playlists = user_dict["playlists"]
    else:
        user.playlists = []
    return user


def get_current_user_jinja():
    # Return the user so that it can be used in jinja templates
    return get_current_user()
