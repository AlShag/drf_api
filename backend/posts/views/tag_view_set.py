from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from posts.models.tag import Tag
from posts.serializers.tag_serializer import TagSerializer

tags = ["Tags"]


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(tags=tags, operation_summary="Retrieve tag and related posts"),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(tags=tags, operation_summary="List of tags"),
)
class TagViewSet(
    RetrieveModelMixin, GenericViewSet, ListModelMixin
):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
