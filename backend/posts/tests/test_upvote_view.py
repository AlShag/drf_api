from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from posts.factories.post_factory import PostFactory
from accounts.factories.user_factory import UserFactory

class UpvoteViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.post = PostFactory()

    def test_upvote_post_and_delete_this_upvote(self):
        self.client.force_authenticate(self.user)
        url = reverse("upvote")
        response = self.client.post(
            url,
            {
                "post": self.post.pk,
            }
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(self.post.upvotes_count, 1)
        response = self.client.post(
            url,
            {
                "post": self.post.pk,
            }
        )
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(self.post.upvotes_count, 0)

    def test_unauthorized_upvote_post_fail(self):
        url = reverse("upvote")
        response = self.client.post(
            url,
            {
                "post": self.post.pk,
            }
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(self.post.upvotes_count, 0)
