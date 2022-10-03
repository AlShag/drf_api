import factory
from ckeditor.fields import RichTextField

from accounts.factories.user_factory import UserFactory
from posts.models.post import Post


class PostFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)

    title = factory.Sequence(lambda n: "Post %03d" % n)
    body =  RichTextField("paragraph")
    is_featured = False

    class Meta:
        model = Post
