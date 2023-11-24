from flask import render_template, redirect, url_for
from membership.services import get_channel_by_id
from admin.services import (
    create_blacklist,
    delete_blacklist,
    get_whitelist_by_channel_id,
    create_whitelist,
    delete_whitelist_by_channel_id,
)
import core


def whitelist_channel(channel_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    whitelist = get_whitelist_by_channel_id(channel_id)
    if whitelist is None:
        create_whitelist(channel_id, user.id)
        delete_blacklist(channel_id, user.id)
    else:
        delete_whitelist_by_channel_id(channel_id)

    return redirect(url_for("dashboard_channel", channel_id=channel_id))


def blacklist_channel(channel_id):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))
    elif not user.is_admin:
        return redirect(url_for("home"))

    channel = get_channel_by_id(channel_id)
    if channel.blacklisted:
        delete_blacklist(channel_id, user.id)
    else:
        create_blacklist(channel_id, user.id)

    return redirect(url_for("dashboard_channel", channel_id=channel_id))
