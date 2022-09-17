import typing as t

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.serializers.user_base_serializer import UserBaseSerializer
from accounts.serializers.user_serializer import UserSerializer

User = get_user_model()


tags = ["Users"]


@method_decorator(
    name="update",
    decorator=swagger_auto_schema(tags=tags, auto_schema=None),  # noqa
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(tags=tags, operation_summary="Update user"),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(tags=tags, operation_summary="List users"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(tags=tags, operation_summary="Retrieve user"),
)
class UserViewSet(
    UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    def get_serializer_class(self) -> t.Type[serializers.Serializer]:
        if self.action in ["list", "retrieve"]:
            return UserBaseSerializer
        else:
            return UserSerializer


    def get_queryset(self) -> QuerySet:
        return User.objects.all()
