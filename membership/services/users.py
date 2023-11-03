from core.db import get_session, get_test_session
from sqlalchemy.orm import Session
import membership.models.user as user_model
import datetime
import re


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
    validate_username(username)

    # Validate password
    validate_password(password)

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
        nickname=nickname,
        created_at=datetime.datetime.now(),
        last_modified_at=datetime.datetime.now(),
    )

    session.add(user)
    session.commit()


def set_user_as_creator(user_id, test=False):
    """
    Sets the given user as the creator of the user with the given id.

    If there is no such user, it raises an exception.
    """
    user = get_user_by_id(user_id)
    if user is None:
        raise Exception("User not found")

    session = get_session() if not test else get_test_session()

    user.is_creator = True
    user.last_modified_at = datetime.datetime.now()
    session.commit()


def get_user_by_username(username):
    """
    Returns the user with the given username.

    If there is no user with the given username, it returns None.
    """
    session = get_session()
    return session.query(user_model.User).filter_by(username=username).first()


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
