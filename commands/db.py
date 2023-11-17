from core.db import db
from membership.services import create_or_update_superuser
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
