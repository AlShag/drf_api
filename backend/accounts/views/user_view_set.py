import typing as t

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core import exceptions
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
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
@method_decorator(
    name="follow",
    decorator=swagger_auto_schema(tags=tags, operation_summary="Follow user"),
)
@method_decorator(
    name="block",
    decorator=swagger_auto_schema(tags=tags, operation_summary="Block user"),
)
@method_decorator(
    name="accept_request",
    decorator=swagger_auto_schema(tags=tags, operation_summary="Accept pending request from user"),
)
@method_decorator(
    name="decline_request",
    decorator=swagger_auto_schema(tags=tags, operation_summary="Decline pending request from user"),
)
class UserViewSet(
    UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    def get_serializer_class(self) -> t.Type[serializers.Serializer]:
        if self.action in ["retrieve", "update", "partial_update"]:
            return UserSerializer
        else:
            return UserBaseSerializer


    def get_queryset(self) -> QuerySet:
        return User.objects.all()

    @action(
        detail=True,
        url_name="follow",
        url_path="follow",
        methods=("POST",),
    )
    def follow(self, request, pk):
        current_user = self.request.user
        target_user = User.objects.get(pk=pk)

        if target_user == current_user:
            raise exceptions.ValidationError("You can not follow yourself")

        if target_user.blocked_users.filter(pk=current_user.pk):
            raise exceptions.ValidationError(f"{target_user.username} blocked you")

        if target_user.followers.filter(pk=current_user.pk):
            target_user.followers.remove(current_user)
            return Response({"Following": "Unfollowing success"},
                            status=status.HTTP_200_OK)

        if target_user.is_private:
            if current_user in target_user.pending_requests.all():
                pass
            else:
                target_user.pending_requests.add(current_user)
                return Response({"Requested": "Follow request has been sent"},
                                status=status.HTTP_200_OK)

        target_user.followers.add(current_user)
        return Response({"Following": "Following success"},
                        status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_name="block",
        url_path="block",
        methods=("POST",),
    )
    def block(self, request, pk):
        current_user = self.request.user
        target_user = User.objects.get(pk=pk)

        if target_user == current_user:
            raise exceptions.ValidationError("You can not block yourself")

        if target_user.followers.filter(pk=current_user.pk):
            target_user.followers.remove(current_user)
        elif target_user.pending_requests.filter(pk=current_user.pk):
            target_user.pending_requests.remove(current_user)

        if current_user.followers.filter(pk=target_user.pk):
            current_user.followers.remove(target_user)
        elif current_user.pending_requests.filter(pk=target_user.pk):
            current_user.pending_requests.remove(target_user)

        if current_user.pending_requests.filter(pk=target_user.pk):
            current_user.pending_requests.remove(target_user)

        if current_user.blocked_users.filter(pk=target_user.pk):
            current_user.blocked_users.remove(target_user)
            return Response({"Following": "Unblock success"},
                            status=status.HTTP_200_OK)

        current_user.blocked_users.add(target_user)
        return Response({"Following": "Block success"},
                        status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_name="accept-request",
        url_path="accept-request",
        methods=("POST",),
    )
    def accept_request(self, request, pk):
        current_user = self.request.user
        target_user = User.objects.get(pk=pk)

        if not current_user.pending_requests.filter(pk=target_user.pk):
            raise exceptions.ValidationError(f"You have no request from {target_user.username}")

        current_user.pending_requests.remove(target_user)
        current_user.followers.add(target_user)
        return Response({"Following": "Accept success"},
                        status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_name="decline-request",
        url_path="decline-request",
        methods=("POST",),
    )
    def decline_request(self, request, pk):
        current_user = self.request.user
        target_user = User.objects.get(pk=pk)

        if not current_user.pending_requests.filter(pk=target_user.pk):
            raise exceptions.ValidationError(f"You have no request from {target_user.username}")

        current_user.pending_requests.remove(target_user)
        return Response({"Following": "Decline success"},
                        status=status.HTTP_200_OK)
