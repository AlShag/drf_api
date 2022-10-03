from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models.post import Post, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    related_posts = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
            "image_url",
            "related_posts",
        )

    def get_related_posts(self, obj):
        related_posts = Post.objects.filter(tags__id__in=[obj.pk])
        return related_posts.values()
