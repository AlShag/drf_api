from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.serializers.user_base_serializer import UserBaseSerializer

User = get_user_model()


class UserSerializer(UserBaseSerializer):
    avatar_url = serializers.ImageField(source="avatar", allow_null=True)
    followers = UserBaseSerializer(many=True, read_only=True)
    pending_requests = UserBaseSerializer(many=True, read_only=True)
    blocked_users = UserBaseSerializer(many=True, read_only=True)
    following = serializers.ReadOnlyField()

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "avatar_url",
            "followers",
            "pending_requests",
            "blocked_users",
            "following",
            "is_private",
        )
