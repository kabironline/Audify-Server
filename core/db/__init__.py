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

def get_session():
    """Returns a session object bound to the engine"""
    return db.session


def get_test_session():
    """Returns a session object bound to the test engine"""
    return test_db.session
