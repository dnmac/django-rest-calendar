import pytest
from pytest_factoryboy import register
from django.core.management import call_command
from tests.factories import *

register(UserFactory)
register(CalendarFactory)
register(EventFactory)
register(UserEventFactory)
register(CurrentWeekFactory)


def test_test():
    assert True


@pytest.fixture
def calendar(db, calendar_factory):
    calendar = calendar_factory.create()
    return calendar


@pytest.fixture
def calendar_create(db, calendar_factory):
    calendar = calendar_factory.create()
    return calendar


@pytest.fixture
def user_create_build(db, user_factory):
    user = user_factory.build()
    return user


@pytest.fixture
def user_create(db, user_factory):
    user = user_factory.build()
    return user


@pytest.fixture
def user_create_stub(db, user_factory):
    user = user_factory.stub()
    return user


@pytest.fixture
def user_event_create(db, user_event_factory):
    event = user_event_factory.build()
    return event


@pytest.fixture
def current_week_create(db, current_week_factory):
    currentweek = current_week_factory.create()
    return currentweek
