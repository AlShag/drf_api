from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.serializers.login_serializer import LoginSerializer
from accounts.serializers.user_base_serializer import UserBaseSerializer

tags = ["Authentication"]


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Login",
        operation_description="",
        responses={200: UserBaseSerializer()},
    ),
)
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    @method_decorator(sensitive_post_parameters("password"))
    def dispatch(self, *args, **kwargs) -> Response:
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs) -> Response:
        login_serializer = self.get_serializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user, remember_me = login_serializer.save()
        request.session.clear()
        login(request, user)
        if not remember_me:
            request.session.set_expiry(0)

        response_serializer = UserBaseSerializer(
            instance=user, context={"request": request}
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
