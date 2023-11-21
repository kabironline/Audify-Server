from core.db import db
from membership.services import (
    create_or_update_superuser,
    get_all_channels,
    update_channel,
)
from music.services.track import get_all_tracks
import click
from flask.cli import with_appcontext


@click.command(name="create_tables")
@with_appcontext
def create_tables():
    """Creates the database tables"""
    print("Creating tables")
    db.create_all()


@click.command(name="drop_all_tables")
@with_appcontext
def drop_all_tables():
    """Drops all the database tables"""
    db.drop_all()


@click.command(name="drop_table")
@click.argument("table_name")
@with_appcontext
def drop_table(table_name):
    """Drops the given database table"""
    db.drop_table(table_name)


@click.command(name="create_superuser")
@click.argument("username")
@click.argument("password")
@with_appcontext
def create_superuser(username, password):
    """Drops the given database table"""
    create_or_update_superuser(username, password)


@click.command(name="update_channelname")
@with_appcontext
def update_channelname():
    channels = get_all_channels()
    for channel in channels:
        channel_name = channel.name
        # Split the names by capital letters
        # Example: "MyChannel" -> ["My", "Channel"]
        channel_name_parts = []
        current_part = ""
        for letter in channel_name:
            if letter.isupper() or letter == "-":
                channel_name_parts.append(current_part)
                current_part = ""
            current_part += letter
        channel_name_parts.append(current_part)
        # Join the parts by spaces
        # Example: ["My", "Channel"] -> "My Channel"
        channel_name = " ".join(channel_name_parts)

        # update the channel
        update_channel(channel.id, name=channel_name, description=channel.description)
