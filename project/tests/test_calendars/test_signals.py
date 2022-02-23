from pprint import pprint
import pytest
from calendars.models import CurrentWeekEvent


def test_calendar_name(calendar):
    """
    Test calendar signal, sets calendar name to username
    automatically when user is created.
    """
    pprint(vars(calendar.user))
    print(f'calendar_name: {calendar.name} == username: {calendar.user.username}')
    assert calendar.__str__() == calendar.user.username


@pytest.mark.usefixtures("current_week_create")
class TestCurrentWeekEvent:
    """Test that creating a CurrentWeek, creates 7 CurrentWeek events."""

    def test_create_current_week(self, current_week_create):
        current_week = current_week_create
        cw = current_week
        print(cw)
        pprint(vars(cw))
        cwe = CurrentWeekEvent.objects.all()
        print(cwe)

        assert len(cwe) == 7
