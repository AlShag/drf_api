from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models.uuid_abstract_model import UUIDAbstractModel

VERIFY_EMAIL_PATH = "/account/sign-up/continue"
RESET_PASSWORD_PATH = "/account/reset-password/new-password"


class User(UUIDAbstractModel, AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, blank=False)

    avatar = models.ImageField(blank=True, upload_to="user-avatars/")
    is_private = models.BooleanField(default=False, blank=False)

    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="followers_set"
    )
    pending_requests = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="pending_requests_set"
    )
    blocked_users = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="blocked_users_set"
    )

    @property
    def following(self):
        return User.objects.filter(followers=self)
