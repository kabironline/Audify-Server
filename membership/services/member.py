from core.db import get_session, get_test_session
from core import get_current_user
import membership.models.member as member_model
import membership.services as services
import datetime


def create_member(user_id, channel_id):
    """
    Creates a new member with the given user_id and channel_id.

    If there is already a member with the given user_id and channel_id, it raises an exception.
    """
    session = get_session()
    if (
        session.query(member_model.Member)
        .filter_by(user_id=user_id, channel_id=channel_id)
        .first()
        is not None
    ):
        return None
        # raise Exception("Member already exists")

    # Check if the user exists
    user = services.get_user_by_id(user_id)
    if user is None:
        raise Exception("User not found")

    # Check if the channel exists
    channel = services.get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("Channel not found")

    # Checking if the user is a member of the channel
    if (
        session.query(member_model.Member)
        .filter_by(user_id=user_id, channel_id=channel_id)
        .first()
        is not None
    ):
        raise Exception("User is already a member of the channel")

    new_member = member_model.Member(
        user_id=user_id,
        channel_id=channel_id,
        created_by=user_id,
        last_modified_by=user_id,
        created_at=datetime.datetime.now(),
        last_modified_at=datetime.datetime.now(),
    )
    session.add(new_member)
    session.commit()

    return new_member


def get_channel_members(channel_id):
    """
    Returns the members of the channel with the given id.

    If there is no channel with the given id, it raises an exception.
    """
    session = get_session()
    channel = services.get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("Channel not found")

    return session.query(member_model.Member).filter_by(channel_id=channel_id).all()


def get_user_channels(user_id):
    """
    Returns the channels of the user with the given id.

    If there is no user with the given id, it raises an exception.
    """
    session = get_session()
    user = services.get_user_by_id(user_id)
    if user is None:
        raise Exception("User not found")

    return session.query(member_model.Member).filter_by(user_id=user_id).all()


def is_creator(user_id):
    """
    If the user is a member account it returns true
    """

    session = get_session()

    return session.query(member_model.Member).filter_by(user_id=user_id)


def get_member_dict(member):

    toString = lambda x: x.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "id": member.id,
        "user_id": member.user_id,
        "channel_id": member.channel_id,
        "created_by": member.created_by,
        "last_modified_by": member.last_modified_by,
        "created_at": toString(member.created_at),
        "last_modified_at": toString(member.last_modified_at),
    }


def delete_channel_members(channel_id):
    """
    Deletes all the members of the channel with the given id.

    If there is no channel with the given id, it raises an exception.
    """
    session = get_session()
    channel = services.get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("Channel not found")

    session.query(member_model.Member).filter_by(channel_id=channel_id).delete()
    session.commit()
