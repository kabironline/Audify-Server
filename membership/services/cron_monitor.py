from core.db import get_session
from core.mail import send_email
from membership.models import CronMonitor
from membership.services import get_user_by_id, get_all_users
from datetime import datetime
from jinja2 import Template
import os

def create_cron_monitor_entry(user_id):
    """
    Creates a new cron monitor entry for the given user.
    """
    session = get_session()
    new_cron_monitor = CronMonitor(
        user_id=user_id,
        last_active_at=datetime.now(),
        last_notified_at=datetime.now(),
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
    )
    session.add(new_cron_monitor)
    session.commit()

    return new_cron_monitor

def update_user_activity(user_id):
    """
    Updates the last active time of the given user.
    """
    session = get_session()
    cron_monitor = session.query(CronMonitor).filter_by(user_id=user_id).first()
    if cron_monitor is not None:
        cron_monitor.last_active_at = datetime.now()
        session.commit()
        return cron_monitor
    else:
        return None 


def get_cron_monitor_entry(user_id):
    """
    Returns the cron monitor entry for the given user.
    """
    session = get_session()
    cron_monitor = session.query(CronMonitor).filter_by(user_id=user_id).first()
    return cron_monitor

def get_all_cron_monitor_entries():
    """
    Returns all the cron monitor entries.
    """
    session = get_session()
    return session.query(CronMonitor).all()

def delete_cron_monitor_entry(user_id):
    """
    Deletes the cron monitor entry for the given user.
    """
    session = get_session()
    cron_monitor = session.query(CronMonitor).filter_by(user_id=user_id).first()
    if cron_monitor is not None:
        session.delete(cron_monitor)
        session.commit()
        return True
    else:
        return False