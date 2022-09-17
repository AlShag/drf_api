from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.serializers.sign_up_serializer import SignUpSerializer

tags = ["Authentication"]


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
            tags=tags,
            operation_summary="Sign Up",
        ),
    )
class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    @method_decorator(sensitive_post_parameters("password", "password_confirm"))
    def dispatch(self, *args, **kwargs) -> Response:
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
