from .db import *
from .utils import *
from membership.models import User

current_user = None

api = None


def set_api(api_instance):
    global api
    api = api_instance


def get_api():
    return api


def set_current_user(user):
    global current_user
    current_user = user


def get_current_user() -> User:
    return current_user
