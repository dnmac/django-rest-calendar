from datetime import datetime, timedelta
from pprint import pprint
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from calendars.models import Calendar, CurrentWeek, CurrentWeekEvent
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from tests.factories import UserEventFactory, CurrentWeekFactory, get_dates
from faker import Faker

fake = Faker()
User = get_user_model()


@pytest.mark.usefixtures("user_create_stub")
class TestLogin:
    """Tests login endpoint."""

    client = APIClient()

    def test_login(self, user_create_stub):
        data = {
            "username": user_create_stub.username,
            "password": user_create_stub.password
            }
        response = self.client.post("http://127.0.0.1:8000/api-auth/login/", data=data)
        print(f'Status code: {response.status_code}')
        assert response.status_code == 200


@pytest.mark.usefixtures("user_create_stub")
class TestRegistration:
    """Tests registration process."""

    client = APIClient()

    def test_registration(self, user_create_stub):
        # user = UserFactory.stub()
        user = user_create_stub
        data = {
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff
            }
        response = self.client.post('http://localhost/accounts/register/', data)
        pprint(vars(response.data))
        print(f'status_code: {response.status_code}')
        assert response.status_code == 201


class CalendarAdminViewSetTestCase(APITestCase):
    """Tests CalendarAdmin endpoint: api/admin/calendars"""

    list_url = reverse("calendar-admin-list")

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123",
                                            is_staff=True
                                            )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_events_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventAdminViewSetTestCase(APITestCase):
    """Tests EventAdmin endpoint: api/admin/events"""

    list_url = reverse("event-admin-list")

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123",
                                            is_staff=True
                                            )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_events_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventOwnedViewsetTestCase(APITestCase):
    """Tests UserEvent events, endpoint: events."""

    list_url = "event-owned-list"
    detail_url = "event-owned-detail"
    calendar_url = "calendar-detail"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123"
                                            )
        self.calendar = self.user.calendar
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def get_event(self):
        event = UserEventFactory.create(calendar_id=self.calendar.id)
        return event

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_calendar_detail_retrieve(self):
        """Calendar name set to username by default."""
        response = self.client.get(reverse(self.calendar_url, kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test_user")

    def test_userevent_detail_retrieve(self):
        event = self.get_event()
        response = self.client.get(
                                    reverse(
                                            "event-owned-detail",
                                            kwargs={"pk": event.id}
                                            )
                                    )
        pprint(vars(event))
        pprint(vars(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CalendarOwnedViewSetTestCase(APITestCase):
    """Tests CalendarOwnedViewSet endpoint: calendar."""

    list_url = reverse("calendar-list")

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123"
                                            )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_calendar_detail_retrieve(self):
        """Calendar name set to username by default."""
        response = self.client.get(reverse("calendar-detail", kwargs={"pk": 1}))
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test_user")


class EventMonthViewTestCase(APITestCase):
    """
    Create 3 events, 2 for current month, 1 for next month.
    Test the EventMonthView returns two events, endpoint eventslist/monthview
    """

    list_url = reverse("event-month-view-list")
    detail_url = "event-owned-detail"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
                                        username="test_user",
                                        password="TestPass123"
                                        )
        self.calendar = self.user.calendar
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def get_event(self, start_date):
        end_date = get_dates(str(start_date))
        event = UserEventFactory.create(
                                        start_date=start_date,
                                        end_date=end_date,
                                        calendar=self.calendar
                                        )
        return event

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_events_list_retrieve_authenticated(self):
        """
            Create 3 events, two for the current month, 1 for next month.
            Return true if only 2 events are returned.
        """
        event1 = self.get_event(fake.date_this_month())
        event2 = self.get_event(fake.date_this_month())
        event3 = self.get_event(fake.date_this_month()+timedelta(days=33))
        response = self.client.get(self.list_url)

        self.assertEqual(len(response.data["UserEvent"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_detail_retrieve_authenticated(self):
        event = self.get_event(fake.date_this_month())
        response = self.client.get(reverse(self.detail_url, kwargs={'pk': event.id}))
        data = response.json()
        print(data)

        self.assertEqual(data["description"], event.description)

    def test_events_detail_retrieve_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse(self.detail_url, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventListTestCase(APITestCase):
    """Tests EventList for displaying UserEvents, endpoint: eventslist."""

    list_url = reverse("event-list-list")
    detail_url = "event-owned-detail"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123"
                                            )
        self.calendar = self.user.calendar
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def get_event(self, start_date):
        end_date = get_dates(str(start_date))
        event = UserEventFactory.create(
                                        start_date=start_date,
                                        end_date=end_date,
                                        calendar=self.calendar
                                        )
        return event

    def test_events_list_retrieve_authenticated(self):
        event = self.get_event(fake.date_this_month())
        response = self.client.get(self.list_url)
        print(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_detail_retrieve_authenticated(self):
        event = self.get_event(fake.date_this_month())
        response = self.client.get(reverse(self.detail_url, kwargs={'pk': event.id}))
        data = response.json()
        print(type(data))
        print(data)
        assert data["description"] == event.description

    def test_events_detail_retrieve_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse(self.detail_url, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CurrentWeekTestCase(APITestCase):
    """
        Tests CurrentWeekView, endpoint: eventslist/currentweek.
        Only auto generated CurrentWeek events for the current week are returned.
    """

    list_url = reverse("currentweekevent-list")
    detail_url = "currentweekevent-detail"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123"
                                            )
        self.token = Token.objects.create(user=self.user)
        self.calendar = self.user.calendar
        self.api_authentication()

    def get_currentweek(self, start_date):
        event = CurrentWeekFactory.create(start_date=start_date, calendar=self.calendar)
        return event

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_current_week_list_authenticated(self):
        """ Test that we can retrieve 7 CurrentWeekEvent objects."""
        current_week = self.get_currentweek(datetime.now().date())
        response = self.client.get(self.list_url)
        data = response.json()
        print(data)
        self.assertEqual(len(data), 7)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_week_list_retrieve_authenticated(self):
        """
            Create 3 CurrentWeek objects
            1 this week, others +- 1 week
            Test passes if only 1 week returned.
        """
        cw_date = datetime.now().date()
        cw_1 = self.get_currentweek(cw_date)
        cw_2 = self.get_currentweek(cw_date + timedelta(weeks=1))
        cw_3 = self.get_currentweek(cw_date + timedelta(weeks=-1))
        response = self.client.get(self.list_url)
        data = response.json()
        self.assertEqual(len(data), 7)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_week_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_current_week_detail_get_authenticated(self):
        """
            Test cw events are created and that their start_dates
            are only dates this week
        """
        cw_date = datetime.now().date()
        current_week = self.get_currentweek(cw_date)
        get_cw = CurrentWeek.objects.get(id=current_week.id)
        get_cwe = CurrentWeekEvent.objects.filter(current_week=get_cw.id)
        cwe_0 = vars(get_cwe[0])
        cwe_0_id = cwe_0["id"]
        response = self.client.get(reverse(self.detail_url, kwargs={'pk': cwe_0_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_week_detail_post_authenticated(self):
        """
            Test cw events are created and that their start_dates
            are only dates this week
        """
        cw_date = datetime.now().date()
        current_week = self.get_currentweek(cw_date)
        get_cw = CurrentWeek.objects.get(id=current_week.id)
        get_cwe = CurrentWeekEvent.objects.filter(current_week=get_cw.id)
        cwe_0 = vars(get_cwe[0])
        cwe_0_id = cwe_0["id"]
        response = self.client.put(
                                    reverse(
                                        self.detail_url, kwargs={'pk': cwe_0_id}
                                        ),
                                        {'description': 'test description text.'}
                                  )
        data = response.json()
        self.assertEqual(data['description'], 'test description text.')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_week_retrieve_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse(self.detail_url, kwargs={'pk': 1}))
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventAllViewTestCase(APITestCase):
    """Tests the EventAllView endpoint: eventslist/allview """

    list_url = reverse("event-all-view-list")

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123"
                                            )
        self.calendar = self.user.calendar
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def get_currentweek(self, start_date):
        event = CurrentWeekFactory.create(start_date=start_date, calendar=self.calendar)
        return event

    def get_user_event(self, start_date):
        end_date = get_dates(str(start_date))
        event = UserEventFactory.create(start_date=start_date, calendar=self.calendar)
        return event

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_events_list_retrieve_authenticated(self):
        """ Retrieve user event and current week events  """
        cw_date = datetime.now().date()
        cw_event = self.get_currentweek(cw_date)
        user_event = self.get_user_event(cw_date)
        response = self.client.get(self.list_url)
        data = response.json()
        self.assertEqual(len(data["UserEvent"]), 1)
        self.assertEqual(len(data["CurrentWeekEvent"]), 7)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_list_retrieve_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CurrentWeekAllViewTestCase(APITestCase):
    """Tests CurrentWeekAllView endpoint: eventslist/currentweekall."""

    list_url = reverse("current-week-list")

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
                                            username="test_user",
                                            password="TestPass123"
                                            )
        self.calendar = self.user.calendar
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def get_currentweek(self, start_date):
        event = CurrentWeekFactory.create(start_date=start_date, calendar=self.calendar)
        return event

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_current_week_list_retrieve_authenticated(self):
        """ create 3 CurrentWeek objects
            View should return 21 cw events.
        """
        cw_date = datetime.now().date()
        cw_1 = self.get_currentweek(cw_date)
        cw_2 = self.get_currentweek(get_dates("2021-02-01"))
        cw_3 = self.get_currentweek(get_dates("2020-01-12"))
        response = self.client.get(self.list_url)
        data = response.json()
        print(data)
        print(len(data))
        self.assertEqual(len(data), 21)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
