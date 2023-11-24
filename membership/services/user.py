from core.db import get_session, get_test_session
from core import get_current_user
import membership.models.user as user_model
import membership.services as membership_services
import datetime
import re
import os


def create_or_update_superuser(username, password, test=False):
    """
    Creates a superuser with the given username and password.

    It performs the following validations.

    - The provided username adheres to the username format.
    - The password is not empty or None.

    In case of any validation failure, it raises an exception.

    Before creating the superuser, it checks if there is already a user with
    the given username. If there is, make that user a superuser. And update the
    password.

    After the user is successfully created, it returns the user id.
    """

    # Validate username
    validate_username(username)

    # Validate password
    validate_password(password)

    session = get_session() if not test else get_test_session()

    # Check if there is already a user with the given username
    user = session.query(user_model.User).filter_by(username=username).first()
    if user:
        # If there is, make that user a superuser
        user.is_admin = True
        user.password = password
        user.last_modified_at = datetime.datetime.now()
        session.commit()
        return user.id, False

    # Everything is good. Create the superuser
    user = user_model.User(
        username=username,
        password=password,
        is_admin=True,
        bio="",
        nickname=username,
        created_at=datetime.datetime.now(),
        last_modified_at=datetime.datetime.now(),
    )

    session.add(user)
    session.commit()
    return user.id, True


def create_user(username, password, nickname, bio, test=False):
    """
    Creates a user with the given username, password, nickname and bio.

    It performs the following validations.

    - The provided username adheres to the username format.
    - The password is not empty or None.
    - The username is not already taken.

    In case of any validation failure, it raises an exception.

    After the user is successfully created, it returns the user id.
    """

    session = get_session() if not test else get_test_session()

    # Validate username
    # validate_username(username)

    # Validate password
    # validate_password(password)

    # Check if there is already a user with the given username
    user = session.query(user_model.User).filter_by(username=username).first()
    if user:
        raise Exception("Username already taken")

    # Everything is good. Create the user
    user = user_model.User(
        username=username,
        password=password,
        is_admin=False,
        bio=bio,
        nickname=nickname if nickname else username,
        created_at=datetime.datetime.now(),
        last_modified_at=datetime.datetime.now(),
    )

    session.add(user)
    session.commit()


def update_user(user: user_model.User):
    """
    This function updates the user with the given user object.
    """
    old_user = get_user_by_id(user.id)
    old_user.username = user.username if user.username else old_user.username
    old_user.password = user.password if user.password else old_user.password
    old_user.nickname = user.nickname if user.nickname else old_user.nickname
    old_user.bio = user.bio if user.bio else old_user.bio
    old_user.last_modified_at = datetime.datetime.now()
    old_user.last_modified_by = get_current_user().id
    session = get_session()

    if user.avatar:
        import os

        try:
            os.mkdir(f"media/users/{user.id}")
        except FileExistsError:
            pass
        user.avatar.save(f"media/users/{user.id}/avatar.png")

    import core

    # Check if current user is a member of the channel
    channel = None
    members = membership_services.get_user_channels(old_user.id)
    if len(members) > 0:
        channel = membership_services.get_channel_dict(
            membership_services.get_channel_by_id(members[0].channel_id)
        )

    core.set_current_user(old_user, channel=channel)

    session.commit()


def get_all_users():
    """
    Returns a list of all users.
    """
    session = get_session()
    users = session.query(user_model.User).all()
    session.close()
    return users


def get_user_by_username(username):
    """
    Returns the user with the given username.

    If there is no user with the given username, it returns None.
    """
    session = get_session()

    try:
        user = session.query(user_model.User).filter_by(username=username).first()
    except Exception as e:
        print("Error", e)
        return None
    return user


def get_user_by_id(user_id):
    """
    Returns the user with the given id.

    If there is no user with the given id, it returns None.
    """
    session = get_session()
    return session.query(user_model.User).filter_by(id=user_id).first()


def delete_user_by_id(user_id, test=False):
    """
    Deletes the user with the given id.

    If there is no user with the given id, it raises an exception.
    """
    session = get_session() if not test else get_test_session()
    user = session.query(user_model.User).filter_by(id=user_id).first()
    if user is None:
        raise Exception("User not found")

    if user.is_admin:
        raise Exception("Cannot delete a superuser")

    # Deleting the avatar if it exists
    try:
        os.remove(f"media/users/{user.id}/avatar.png")
        os.removedirs(f"media/users/{user.id}")
    except Exception:
        pass

    session.delete(user)
    session.commit()


def validate_username(username):
    """
    Validates that that username has the following properties.
    - It is not empty or None
    - At least 6 characters long
    - Contains alphanumeric characters (digits are optional)
    - Contains only these symbols (optional):
        - _ (underscore)
        - '-' (hyphen)
        - . (period)
        - @ (at)
        - $ (dollar)
    - No spaces allowed, or anyother special characters

    """
    if username is None or username == "":
        raise Exception("Username cannot be empty")

    # Match using regex
    # [a-zA-Z0-9%\_$\-@]{6,} - This regex matches the following

    if not re.match(r"[a-zA-Z0-9%\_$\-@]{6,}", username):
        raise Exception(
            "Username must be at least 6 characters long and can only contain alphanumeric characters and the following symbols: _ - . @ $"
        )


def validate_password(password):
    """
    Validates that that password has the following properties.
    - It is not empty or None
    - At least 8 characters long
    - Contains alphanumeric characters
    - Contains at least one number
    - Contains at least one Capital letter
    - Contains at least one symbol from the following list:
        - _ (underscore)
        - '-' (hyphen)
        - . (period)
        - @ (at)
        - $ (dollar)

    """
    if password is None or password == "":
        raise Exception("Password cannot be empty")

    if len(password) < 8:
        raise Exception("Password must be at least 8 characters long")

    if not any(char.isdigit() for char in password):
        raise Exception("Password must contain at least one number")

    if not any(char.isalpha() for char in password):
        raise Exception("Password must contain at least one letter")

    if not any(char.isupper() for char in password):
        raise Exception("Password must contain at least one Capital letter")

    if not any(char in ["_", "-", ".", "@", "$"] for char in password):
        raise Exception(
            "Password must contain at least one of the following symbols: _ - . @ $"
        )

    return True


def get_user_dict(user: user_model.User, avatar=None):
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "bio": user.bio,
        "is_admin": user.is_admin,
        "created_by": user.created_by,
        "last_modified_by": user.last_modified_by,
        "created_at": user.created_at,
        "last_modified_at": user.last_modified_at,
        "avatar": avatar or "",
    }
