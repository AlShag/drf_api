from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from accounts.factories.user_factory import UserFactory
from posts.factories.post_factory import PostFactory
from posts.factories.tag_factory import TagFactory


class TagViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.tag = TagFactory()
        cls.post = PostFactory()
        cls.post.tags.add( # noqa
            cls.tag.pk # noqa
        )

    def test_tag_list(self) -> None:
        url = reverse("tag-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_tag_retrieve(self) -> None:
        url = reverse("tag-detail", kwargs={"pk": self.tag.pk})
        response = self.client.get(url)
        self.assertEqual(len(response.data["related_posts"]), 1)
        self.assertEqual(response.status_code, HTTP_200_OK)
