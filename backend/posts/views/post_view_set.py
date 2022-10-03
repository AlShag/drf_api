from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.serializers.post_serializer import PostSerializer
from posts.models.post import Post

tags = ["Posts"]


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Create post",
    ),
)
@method_decorator(
    name="update", decorator=swagger_auto_schema(auto_schema=None)  # noqa
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Partial update post",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="List posts",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Retrieve post",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Destroy post",
    ),
)
@method_decorator(
    name="save",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Save post.",
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides control over Post.
    """

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        return Post.objects.all()

    @action(detail=True, methods=("POST",))
    def save(self, *_, **__) -> Response:
        post: Post = self.get_object()
        post.refresh_from_db()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
