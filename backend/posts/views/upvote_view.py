from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from posts.models.upvote import Upvote
from posts.models.post import Post
from posts.serializers.upvote_serializer import UpvoteSerializer

tags = ["Posts"]


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=tags,
        operation_summary="Add or Delete Upvote",
    ),
)
class UpvoteView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Upvote.objects.all()
    serializer_class = UpvoteSerializer

    def post(self, request, *args,**kwargs):
        user = self.request.user
        post = Post.objects.get(pk=request.data["post"])
        try:
            upvote = Upvote.objects.get(user=user, post=post)
            upvote.delete()
            return Response("Upvote removed", status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            upvote = Upvote.objects.create(
                post=post, user=user
            )
            response_serializer = UpvoteSerializer(
                instance=upvote, context={"request": request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
