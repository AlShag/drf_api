from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.views.post_view_set import PostViewSet
from posts.views.upvote_view import UpvoteView

router = DefaultRouter()

router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path("upvote", UpvoteView.as_view(), name="upvote"),
    *router.urls,
]