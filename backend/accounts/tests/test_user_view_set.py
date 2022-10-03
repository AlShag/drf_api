from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase
from accounts.factories.user_factory import UserFactory


class UserViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.user_2 = UserFactory()
        cls.private_user = UserFactory(is_private=True)

    def test_user_list(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)

    def test_user_retrieve(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_user_update(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        response = self.client.patch(
            url,
            {"username": "new_username",},
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "new_username")
        self.user.username = "username"

    def test_user_follow_and_unfollow_another_user(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-follow", kwargs={"pk": self.user_2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.user.following), [self.user_2])
        self.assertEqual(list(self.user_2.followers.all()), [self.user])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.user.following), [])
        self.assertEqual(list(self.user_2.followers.all()), [])

    def test_user_follow_private_user(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-follow", kwargs={"pk": self.private_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.private_user.pending_requests.all()), [self.user])

    def test_user_follow_self_fail(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-follow", kwargs={"pk": self.user.pk})
        with self.assertRaises(Exception) as context:
            self.client.post(url)
        self.assertTrue("You can not follow yourself" in context.exception)
        self.assertEqual(list(self.user.following), [])

    def test_user_block_another_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("user-block", kwargs={"pk": self.user_2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.user.blocked_users.all()), [self.user_2])

    def test_user_block_his_follower_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("user-follow", kwargs={"pk": self.user_2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.user_2.followers.all()), [self.user])

        self.client.force_authenticate(self.user_2)
        url = reverse("user-block", kwargs={"pk": self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.user_2.blocked_users.all()), [self.user])
        self.assertEqual(list(self.user_2.followers.all()), [])

    def test_user_block_self_fail(self):
        self.client.force_authenticate(self.user)
        url = reverse("user-block", kwargs={"pk": self.user.pk})
        with self.assertRaises(Exception) as context:
            self.client.post(url)
        self.assertTrue("You can not block yourself" in context.exception)
        self.assertEqual(list(self.user.blocked_users.all()), [])

    def test_user_accept_pending_request(self):
        self.client.force_authenticate(self.user)
        url = reverse("user-follow", kwargs={"pk": self.private_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.private_user.pending_requests.all()), [self.user])

        self.client.force_authenticate(self.private_user)
        url = reverse("user-accept-request", kwargs={"pk": self.user.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.private_user.pending_requests.all()), [])
        self.assertEqual(list(self.private_user.followers.all()), [self.user])

    def test_user_decline_pending_request(self):
        self.client.force_authenticate(self.user)
        url = reverse("user-follow", kwargs={"pk": self.private_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.private_user.pending_requests.all()), [self.user])

        self.client.force_authenticate(self.private_user)
        url = reverse("user-decline-request", kwargs={"pk": self.user.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(list(self.private_user.pending_requests.all()), [])
        self.assertEqual(list(self.private_user.followers.all()), [])
