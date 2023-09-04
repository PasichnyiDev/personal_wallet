from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status

from personal_wallet.routes_util import routes_util

USER_USERNAME_KEY = "username"
USER_PASSWORD_KEY = "password"

TEST_USER_USERNAME = "TestUserUsername"
TEST_USER_PASSWORD = "KVs45619572bhdn"
TEST_USER_INVALID_USERNAME = ""

REQUEST_FORMAT = "json"


class UserTests(TestCase):

    def setUp(self) -> None:
        self.registration_url = reverse(routes_util.users_registration_url_name())

    def test_users_registration(self):
        user_data = {
            USER_USERNAME_KEY: TEST_USER_USERNAME,
            USER_PASSWORD_KEY: TEST_USER_PASSWORD
        }
        response = self.client.post(path=self.registration_url, data=user_data, format=REQUEST_FORMAT)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_users_registration_invalid_data(self):
        user_data = {
            USER_USERNAME_KEY: TEST_USER_INVALID_USERNAME,
            USER_PASSWORD_KEY: TEST_USER_PASSWORD
        }
        response = self.client.post(path=self.registration_url, data=user_data, format=REQUEST_FORMAT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_users_registration_duplicate_username(self):
        get_user_model().objects.create_user(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        user_data = {
            USER_USERNAME_KEY: TEST_USER_USERNAME,
            USER_PASSWORD_KEY: TEST_USER_PASSWORD
        }

        response = self.client.post(path=self.registration_url, data=user_data, format=REQUEST_FORMAT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1)
