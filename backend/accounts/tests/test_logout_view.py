from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from accounts.factories.user_factory import UserFactory


class LogoutViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.logout_url = reverse("logout")

    def test_logout(self) -> None:
        self.client.force_authenticate(self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertFalse(self.client.session.get("_auth_user_id", False))
