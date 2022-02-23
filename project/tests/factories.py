import factory
import factory.fuzzy
import pytest
from calendars.models import Calendar, Event, UserEvent, CurrentWeek, CurrentWeekEvent
from faker import Faker
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime, date, timedelta

User = get_user_model()
fake = Faker()


def get_dates(start_date_str):
    start_date = date.fromisoformat(start_date_str)
    strip = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = (strip + timedelta(days=1)).date()
    return end_date


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = fake.pyint(min_value=0, max_value=100, step=1)
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    is_staff = False


class CalendarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Calendar
        database = 'default'
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    name = "default"


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event
        django_get_or_create = ('calendar', 'id')

    id = factory.Sequence(lambda n: 1+n)
    calendar = factory.SubFactory(CalendarFactory)
    title = factory.LazyFunction(fake.word)
    description = factory.LazyFunction(fake.paragraph)
    duration = fake.pyint(min_value=0, max_value=9, step=1)
    start_date = date.fromisoformat(fake.date())
    end_date = get_dates(str(start_date))


class UserEventFactory(EventFactory, factory.django.DjangoModelFactory):
    class Meta:
        model = UserEvent

    classification = 'RR'
    priority = 'A'
    type = 'AM'


class CurrentWeekFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrentWeek

    calendar = factory.SubFactory(CalendarFactory)
    start_date = date.fromisoformat(fake.date())


class CurrentWeekEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrentWeekEvent

    current_week = factory.SubFactory(CurrentWeekFactory)
    comments = factory.LazyFunction(fake.paragraph)
