from membership.models.user import *
from membership.models.member import *
from membership.models.channel import *
from sqlalchemy import inspect
from core.db import Base, engine, test_engine
import click
from flask.cli import with_appcontext


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    """Creates the database tables"""
    Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=test_engine)
    click.echo('Tables created')


@click.command(name='drop_all_tables')
@with_appcontext
def drop_all_tables():
    """Drops all the database tables"""
    tables = Base.metadata.sorted_tables
    for table in tables:
        if table.name == 'alembic_version':
            continue
        table.drop(bind=engine)


@click.command(name='drop_table')
@click.argument('table_name')
@with_appcontext
def drop_table(table_name):
    """Drops the given database table"""
    Base.metadata.tables[table_name].drop(bind=engine)
    click.echo(f'Table {table_name} dropped')
