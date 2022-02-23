from pprint import pprint
import pytest


def test_tests():
    assert True


def test_calendar_user(calendar_factory):
    assert calendar_factory.user == calendar_factory.user


@pytest.mark.django_db
def test_calendar_name(calendar_factory):
    assert calendar_factory.name == str(calendar_factory.name)


def test_event_create(user_event_create):
    pprint(vars(user_event_create))
    assert user_event_create.__str__() == user_event_create.title


def test_new_user(user_factory):
    pprint(vars(user_factory))
    assert True


def test_create_new_user(db, user_factory):
    user = user_factory.create()
    print(user.username)
    assert True


def test_build_new_user(db, user_factory):
    user = user_factory.build()
    print(user.username)
    assert True


def test_username_length(user_create):
    assert len(user_create.username) >= 1
