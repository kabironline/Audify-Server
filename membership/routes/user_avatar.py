from flask import send_file, url_for
from membership.services import get_user_by_id
import core


def user_avatar(user_id):
    """
    This function sends the file of the user avatar to the browser.

    If the file is not found, it sends the default avatar.

    - param user_id: The ID of the user whose avatar is requested

    - return: The file of the user avatar
    """

    user = get_user_by_id(user_id)
    if user is None:
        return None

    avatar_path = "media/users/" + str(user_id) + "/avatar.png"

    # try to read the file
    try:
        import os

        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", avatar_path
        )
        print(path)
        with open(path, "rb") as avatar_file:
            avatar_file.read()

    except FileNotFoundError:
        avatar_path = "static/images/default-avatar.webp"
        return send_file(avatar_path, mimetype="image/png")

    return send_file(avatar_path, mimetype="image/png")
