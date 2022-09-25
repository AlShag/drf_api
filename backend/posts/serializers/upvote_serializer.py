from rest_framework import serializers

from posts.models.upvote import Upvote

class UpvoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Upvote
        fields = (
            "pk",
            "post",
        )
