from django.contrib.auth import get_user_model
from django.db import models

from common.models.uuid_abstract_model import UUIDAbstractModel

User = get_user_model()

class Upvote(UUIDAbstractModel):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
