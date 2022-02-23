import pytest
from django.urls import reverse
from django.test import TestCase, Client
from tests.factories import CalendarFactory
from django.contrib.auth import get_user_model

from rest_framework.test import RequestsClient, APIClient
from django.urls import include, path, reverse
from accounts.views import *
from pprint import pprint
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import APITransactionTestCase
from rest_framework import status
from calendars.views import *
from calendars.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.test import APIRequestFactory

User = get_user_model()


class UserUrlsTestCase(APITestCase):
    """Test all list URLs, useful for debugging."""

    list_urls = [
                "calendar-list", "event-owned-list",
                "event-owned-list", "event-month-view-list",
                "event-list-list", "currentweekevent-list",
                "event-all-view-list", "current-week-list"
                ]

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

    def test_events_list_authenticated(self):
        for url in self.list_urls:
            response = self.client.get(reverse(url))
            print(f'endpoint: {url} response: {response.status_code}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        for url in self.list_urls:
            response = self.client.get(reverse(url))
            print(f'endpoint: {url} response: {response.status_code}')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminUrlsTestCase(APITestCase):
    """Test all Admin list URLs, useful for debugging."""

    list_urls = ["calendar-admin-list", "event-admin-list"]

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
        for url in self.list_urls:
            response = self.client.get(reverse(url))
            print(f'endpoint: {url} response: {response.status_code}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_events_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        for url in self.list_urls:
            response = self.client.get(reverse(url))
            print(f'endpoint: {url} response: {response.status_code}')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
