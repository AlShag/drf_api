from django.db import models, transaction
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from ytmusicapi import YTMusic

from common.models.uuid_abstract_model import UUIDAbstractModel
from common.models.with_created_at_and_modified_at_abstract_model import WithCreatedAtAndModifiedAtAbstractModel
from posts.models.tag import Tag
from posts.models.upvote import Upvote

yt = YTMusic()
User = get_user_model()


class PostManager(models.Manager):
    @transaction.atomic
    def create_with_related_objects(self, **kwargs):
        tags = []
        thumbnail = None

        if kwargs["featured_type"] == "ALBUM":
            album = yt.get_album(kwargs["featured_id"])
            album_title = album["title"]
            album_year = album["year"]
            album_artists = []
            for i in range(len(album["artists"])):
                album_artists.append(album["artists"][i]["id"])
            thumbnail = album["thumbnails"][3]["url"] # 544x544px image

            tag = Tag.objects.get_or_create(
                name=album_title,
                image_url=album["thumbnails"][2]["url"], # 226x226px image
            )
            tags.append(tag[0].pk)

            tag = Tag.objects.get_or_create(
                name=album_year,
                image_url = f"https://via.placeholder.com/150/000000/FFFFFF/?text={album_year}",
            )
            tags.append(tag[0].pk)

            for artist in album_artists:
                artist_detail = yt.get_artist(artist)
                artist_name = artist_detail["name"]
                artist_thumbnail =  artist_detail["thumbnails"][0]["url"]
                tag = Tag.objects.get_or_create(
                    name=artist_name,
                    image_url=artist_thumbnail
                )
                tags.append(tag[0].pk)

        elif kwargs["featured_type"] == "ARTIST":
            artist = yt.get_artist(kwargs["featured_id"])
            artist_name = artist["name"]
            artist_thumbnail = artist["thumbnails"][0] # 540x225px image

            tag = Tag.objects.get_or_create(
                name=artist_name,
                image_url=artist_thumbnail,
            )
            tags.append(tag[0].pk)

            thumbnail = artist["thumbnails"][1]["url"] # 816x340px image

        elif kwargs["featured_type"] == "SONG":
            song = yt.get_song(kwargs["featured_id"])
            song_name = song["videoDetails"]["title"]
            song_artist = yt.get_artist(song["videoDetails"]["channelId"])
            song_artist_name = song_artist["name"]
            song_artist_thumbnail = song_artist["thumbnails"][0] # 540x225px image
            song_publish_date = song["microformat"]["microformatDataRenderer"]["publishDate"]
            # example of song_publish_date: "2018-06-21"
            song_year = ''.join(song_publish_date.split('-')[:-2])
            # example of song_year based on song_publish_date example: "2018"
            thumbnail = song["videoDetails"]["thumbnail"]["thumbnails"][2]["url"]

            tag = Tag.objects.get_or_create(
                name=song_year,
                image_url = f"https://via.placeholder.com/150/000000/FFFFFF/?text={song_year}",
            )
            tags.append(tag[0].pk)

            tag = Tag.objects.get_or_create(
                name=song_name,
                image_url = song["videoDetails"]["thumbnail"]["thumbnails"][2]["url"], # 226x226px image
            )
            tags.append(tag[0].pk)

            tag = Tag.objects.get_or_create(
                name=song_artist_name,
                image_url=song_artist_thumbnail,
            )
            tags.append(tag[0].pk)

        elif kwargs["featured_type"] == "PLAYLIST":
            playlist = yt.get_playlist(kwargs["featured_id"])
            thumbnail = playlist["thumbnails"][1]["url"] # 576x576px image

        kwargs["thumbnail"] = thumbnail
        kwargs.pop("tags")
        post = self.create(**kwargs)

        for tag in tags:
            post.tags.add(tag)

        return post


class Post(UUIDAbstractModel, WithCreatedAtAndModifiedAtAbstractModel):
    FEATURED_TYPE_CHOICES = (
        ("ALBUM" ,"album"),
        ("ARTIST", "artist"),
        ("SONG", "song"),
        ("PLAYLIST", "playlist"),
    )

    title = models.CharField(max_length=150)
    body = RichTextField(null=False, blank=False)
    thumbnail = models.ImageField(
        blank=True,
        upload_to="thumbnails/%Y/%m/%d",
        max_length=255
    )
    author = models.ForeignKey(
        "accounts.User",
        related_name="posts",
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        "posts.Tag",
        blank=True,
        related_name="posts",
    )
    is_featured = models.BooleanField(null=True, blank=True)
    featured_type = models.CharField(choices=FEATURED_TYPE_CHOICES, blank=True, max_length=200)
    featured_id = models.CharField(null=True, blank=True, max_length=200)

    objects = PostManager()

    @property
    def upvotes_count(self):
        return Upvote.objects.filter(post=self).count()

    def __str__(self):
        return self.title
