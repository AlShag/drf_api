from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "password_confirm",
        )

    def validate(self, data: dict) -> dict:

        # compare passwords
        if data["password"] != data["password_confirm"]:
            raise ValidationError("Passwords must match")

        # remove extra unneeded field
        data.pop('password_confirm')

        # validate "password"
        user = User(**data)
        password = data.get("password")
        try:
            password_validation.validate_password(password=password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        del user

        return data

    def create(self, validated_data: dict) -> User:
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user
