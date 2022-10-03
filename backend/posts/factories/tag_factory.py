import factory

from posts.models.tag import Tag


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Tag %03d" % n)
    image_url = factory.Faker("url")

    class Meta:
        model = Tag
