from membership.services import *
from membership.models.user import User
from core.db import get_test_session


def test_create_or_update_superuser():
    session = get_test_session()

    id, created = create_or_update_superuser(
        "test_superuser_1", "Admin@123", True)

    assert id is not None and created is True
    assert session.query(User).filter_by(
        username="test_superuser_1").first() is not None
    id, created = create_or_update_superuser(
        "test_superuser_1", "Admin@123", True)

    assert id is not None and created is False
    assert session.query(User).filter_by(
        username="test_superuser_1").first() is not None

    user = session.query(User).filter_by(username="test_superuser_1").first()
    session.delete(user)
    session.commit()


def test_create_user():
    id = create_user("test_user_1", "Admin@123",
                     "test_user_1", "test_user_1", True)

    session = get_test_session()

    user = session.query(User).filter_by(username="test_user_1").first()

    assert user is not None

    try:
        create_user("test_user_1", "Admin@123",
                    "test_user_1", "test_user_1", True)
        assert False
    except Exception as e:
        assert True

    session.delete(user)
    session.commit()


def test_validate_username():
    assert validate_username("admin@123") is True


def test_validate_password():
    assert validate_password("Admin@123") is True

# def test_validate_username():
#     assert validate_username("admin") is True
