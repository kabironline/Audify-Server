# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import DeclarativeBase, Session
# from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
test_db = SQLAlchemy()
def get_db():
    """
    Returns the database object.

    If the database is not initialized, it raises an exception.
    """
    return db

# DeclarativeBase = declarative_base()


# class Base(DeclarativeBase):
#     pass


# engine = create_engine('sqlite:///core/db/db.sqlite3', echo=True)
# test_engine = create_engine('sqlite:///core/db/test_db.sqlite3', echo=True)

# with engine.connect() as conn:
#     result = conn.execute(text('SELECT "Hello"'))
#     print(result.all())

# with test_engine.connect() as conn:
#     result = conn.execute(text('SELECT "Hello"'))
#     print(result.all())


def get_session():
    """Returns a session object bound to the engine"""
    return db.session


def get_test_session():
    """Returns a session object bound to the test engine"""
    return test_db.session

# def get_db():
#     """
#     Returns the database object.

#     If the database is not initialized, it raises an exception.
#     """
#     if db is None:
#         raise Exception("Database not initialized")
#     return db


# def get_db_session():
#     """
#     Returns the database session object.

#     If the database is not initialized, it raises an exception.
#     """
#     return get_db().session
