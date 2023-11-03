from .db import *
from .utils import *

current_user = None


def set_current_user(user):
    global current_user
    current_user = user


def get_current_user():
    return current_user
