import commands.create_db
from core.db import engine
from sqlalchemy import inspect


def test_create_tables():
    # Checking if the tables are created
    table_names = ['User', 'Member', 'Channel']
    user_table_columns = {'id', 'username', 'nickname', 'bio', 'password',
                          'is_admin', 'created_by', 'last_modified_by', 'created_at', 'last_modified_at'}
    channel_table_columns = {'id', 'name', 'description', 'created_by',
                             'last_modified_by', 'created_at', 'last_modified_at'}
    member_table_columns = {'id', 'is_admin', 'user_id', 'channel_id', 'created_by',
                            'last_modified_by', 'created_at', 'last_modified_at'}
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():

        if table_name not in table_names:
            continue
        table_names.remove(table_name)
        columns = inspector.get_columns(table_name)
        print([column['name'] for column in columns])
        if table_name == 'User':
            assert user_table_columns == set(
                [column['name'] for column in columns])
            pass
        elif table_name == 'Channel':
            assert channel_table_columns == set(
                [column['name'] for column in columns])
            pass
        elif table_name == 'Member':
            assert member_table_columns == set(
                [column['name'] for column in columns])
            pass
    assert len(table_names) == 0
