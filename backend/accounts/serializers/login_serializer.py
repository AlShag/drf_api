import typing as t

from django.contrib.auth import authenticate, get_user_model
from django.core import exceptions
from django.db.models import Q
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})
    remember_me = serializers.BooleanField(default=False)

    def validate(self, attrs: dict) -> dict:
        invalid_login_error_message = (
            "Unable to log in with provided credentials."
        )

        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")

        try:
            user = User.objects.get(
                Q(email__iexact=username_or_email)
                | Q(username__iexact=username_or_email)
            )
        except User.DoesNotExist:
            raise exceptions.ValidationError(invalid_login_error_message)
        is_correct_password = user.check_password(password)

        if not is_correct_password:
            raise exceptions.ValidationError(invalid_login_error_message)

        attrs["user"] = user
        return attrs

    def save(self, **kwargs) -> t.Tuple[User, bool]:
        return (
            self.validated_data["user"],
            self.validated_data["remember_me"],
        )
