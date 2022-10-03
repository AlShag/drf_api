from django.contrib import admin

from posts.models.post import Post
from posts.models.tag import Tag
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    fields = (
            "title",
            "body",
            "author",
            "created_at",
            "modified_at",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = (
        "name",
        "image_url",
    )