from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

User = get_user_model()


class SignUpViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.sign_up_url = reverse("sign-up")
        cls.sign_up_payload = {
            "email": "user@email.com",
            "username": "user",
            "password": "super_secure_password@123",
            "password_confirm": "super_secure_password@123",
        }

    def test_sm_sign_up(
        self,
    ) -> None:
        users_count = User.objects.count()
        response = self.client.post(
            self.sign_up_url, self.sign_up_payload
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), users_count + 1)

    def test_sm_sign_up_with_duplicate_email_fails(self) -> None:
        payload = self.sign_up_payload
        payload["email"] = "duplicateemail@exmaple.com"
        response = self.client.post(self.sign_up_url, payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        response = self.client.post(self.sign_up_url, payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
