from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.serializers.user_base_serializer import UserBaseSerializer

User = get_user_model()


class UserSerializer(UserBaseSerializer):
    avatar_url = serializers.ImageField(source="avatar", allow_null=True)

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "avatar_url",
            "followers",
            "pending_requests",
            "blocked_users",
            "is_private",
        )
