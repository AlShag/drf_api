from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from accounts.factories.user_factory import UserFactory

User = get_user_model()


class LoginTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.login_url = reverse("login")

    def test_login_username(self) -> None:
        payload = {
            "username_or_email": self.user.username,
            "password": UserFactory.password.method_arg,
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(self.user.id),
        )

    def test_login_email(self):
        payload = {
            "username_or_email": self.user.email,
            "password": UserFactory.password.method_arg,
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(self.user.id),
        )

    def test_login_invalid(self) -> None:
        payload = {
            "username_or_email": self.user.username,
            "password": "wrong password",
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertFalse(self.client.session.get("_auth_user_id", False))

    def test_login_unregistered(self) -> None:
        payload = {
            "username_or_email": "unregistered@email.com",
            "password": UserFactory.password.method_arg,
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertFalse(self.client.session.get("_auth_user_id", False))
