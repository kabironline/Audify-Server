from core.db import get_session
from core.mail import send_email
from membership.models import CronMonitor
from music.services import get_channel_month_top_tracks, get_channel_month_total_views
from membership.services import get_user_by_id, get_all_users, get_all_channels, get_channel_members, get_channel_by_id
from datetime import datetime
from jinja2 import Template
import os
    
def notify_user(user_id):
    """
    Notifies the user with the given user_id.
    """
    session = get_session()
    cron_monitor = session.query(CronMonitor).filter_by(user_id=user_id).first()
    if cron_monitor is not None:
        # Notify the user if the user has been inactive for a day but if the user has been dont send subsequent notifications for the next 7 days

        if (cron_monitor.last_active_at - cron_monitor.last_notified_at).days >= 1 and (datetime.now() - cron_monitor.last_notified_at).days >= 7:
            # Send the notification
            print(f"Sending notification to user {user_id}")
            # load the email template which is stored in the templates/email folder
            user = get_user_by_id(user_id)
            template = None
            # open the file located at "../../templates/email/user_inactive.html"
            with open(os.path.join(os.path.dirname(__file__), "../../templates/email/user_inactive.html"), "r") as file:
                template = Template(file.read())
            template = template.render(username=user.username)
            send_email(user.username, "Inactive User Notification", template)
            cron_monitor.last_notified_at = datetime.now()
        session.commit()
        return cron_monitor
    else:
        return None

def update_cron_monitor_list():
    """
    Updates the cron monitor list.
    """

    from membership.services import get_all_cron_monitor_entries, create_cron_monitor_entry
    users = get_all_users()
    cron_monitor_entries = get_all_cron_monitor_entries()
    user_ids = [entry.user_id for entry in cron_monitor_entries]
    for user in users:
        if user.id not in user_ids:
            create_cron_monitor_entry(user.id)

def daily_user_activity_check():
    """
    Checks the activity of all the users and sends notifications if required.
    """
    from membership.services import get_all_cron_monitor_entries
    cron_monitor_entries = get_all_cron_monitor_entries()
    for entry in cron_monitor_entries:
        notify_user(entry.user_id)
    return True

def generate_send_channel_report(channel_id):
    """
    Returns the monthly report for the channel with the given id.
    """
    session = get_session()
    channel = get_channel_by_id(channel_id)
    if channel is None:
        return None

    date = datetime.now()
    month = date.month
    year = date.year

    top_tracks = get_channel_month_top_tracks(channel_id, month, year)
    total_views = get_channel_month_total_views(channel_id, month, year)

    template = None 
    if total_views == 0 or len(top_tracks) == 0:
        with open(os.path.join(os.path.dirname(__file__), "../../templates/email/channel_monthly_no_activity.html"), "r") as file:
            template = Template(file.read())
        template = template.render()

    else:
        with open(os.path.join(os.path.dirname(__file__), "../../templates/email/channel_monthly_report.html"), "r") as file:
            template = Template(file.read())
        template = template.render(
            channel_name=channel.name,
            month=month,
            year=year,
            top_tracks=top_tracks,
            total_views=total_views,
            month_name=datetime(1900, month, 1).strftime('%B')
        )
    # get channel members
    members = get_channel_members(channel_id)
    for member in members:
        user = get_user_by_id(member.user_id)
        send_email(user.username, "Monthly Channel Report", template)


def monthly_channel_report():
    """
    Sends the monthly report for all the channels.
    """
    channels = get_all_channels()
    for channel in channels:
        generate_send_channel_report(channel.id)
    return True