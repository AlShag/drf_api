from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

tags = ["Authentication"]
success_msg = "Successfully logged out"


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Logout",
        operation_description="",
        responses={200: success_msg}
    )
)
class LogoutView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(success_msg, status=status.HTTP_200_OK)
