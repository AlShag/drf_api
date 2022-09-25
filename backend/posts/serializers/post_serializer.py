from rest_framework import serializers

from posts.models.post import Post
from posts.models.tag import Tag

class PostSerializer(serializers.ModelSerializer):
    upvotes_count = serializers.ReadOnlyField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    class Meta:
        model = Post
        fields = (
            "pk",
            "title",
            "thumbnail",
            "body",
            "author",
            "tags",
            "is_featured",
            "featured_type",
            "featured_id",
            "upvotes_count",
        )

    def create(self, validated_data):

        if validated_data["is_featured"]:
            post = Post.objects.create_with_related_objects(
                **validated_data,
            )

            return post
        else:
            return Post.objects.create(author=self.context["request"].user)
