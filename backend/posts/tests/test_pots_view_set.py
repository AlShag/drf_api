from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APITestCase

from posts.models.tag import Tag
from accounts.factories.user_factory import UserFactory
from posts.factories.post_factory import PostFactory
from posts.factories.tag_factory import TagFactory


class PostViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.post = PostFactory()
        cls.tag = TagFactory()

    def test_post_list(self) -> None:
        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_retrieve(self) -> None:
        url = reverse("post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_update(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("post-detail", kwargs={"pk": self.post.id})
        response = self.client.patch(
            url,
            {"title": "new_title",},
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "new_title")
        self.post.title = "title"

    def test_post_create(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("post-list")
        response = self.client.post(
            url,
            {
                "title": "custom_title",
                "body": "paragraph",
                "author": self.user.pk,
             }
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_album_featured_post_tags_auto_create(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("post-list")
        response = self.client.post(
            url,
            {
                "title": "custom_title",
                "body": "paragraph",
                "author": self.user.pk,
                "is_featured": True,
                "featured_type": "ALBUM",
                "featured_id": "MPREb_KCNeTnK02S7" # Kanye West - Graduation
             }
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(len(response.data["tags"]), 3)
        album_title_tag = Tag.objects.get(pk=response.data["tags"][0]).name
        album_year_tag = Tag.objects.get(pk=response.data["tags"][1]).name
        album_artist_tag = Tag.objects.get(pk=response.data["tags"][2]).name
        self.assertEqual(album_title_tag, "Graduation")
        self.assertEqual(album_year_tag, "2007")
        self.assertEqual(album_artist_tag, "Kanye West")

    def test_artist_featured_post_tags_auto_create(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("post-list")
        response = self.client.post(
            url,
            {
                "title": "custom_title",
                "body": "paragraph",
                "author": self.user.pk,
                "is_featured": True,
                "featured_type": "ARTIST",
                "featured_id": "UCRY5dYsbIN5TylSbd7gVnZg" # Kanye West
             }
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(len(response.data["tags"]), 1)
        artist_tag = Tag.objects.get(pk=response.data["tags"][0]).name
        self.assertEqual(artist_tag, "Kanye West")

    def test_song_featured_post_tags_auto_create(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("post-list")
        response = self.client.post(
            url,
            {
                "title": "custom_title",
                "body": "paragraph",
                "author": self.user.pk,
                "is_featured": True,
                "featured_type": "SONG",
                "featured_id": "LQ488QrqGE4" # Kanye West - Homecoming
             }
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(len(response.data["tags"]), 3)
        song_year_tag = Tag.objects.get(pk=response.data["tags"][0]).name
        song_name_tag = Tag.objects.get(pk=response.data["tags"][1]).name
        song_artist_tag = Tag.objects.get(pk=response.data["tags"][2]).name
        self.assertEqual(song_year_tag, "2009")
        self.assertEqual(song_name_tag, "Homecoming [Clean]")
        self.assertEqual(song_artist_tag, "Kanye West")