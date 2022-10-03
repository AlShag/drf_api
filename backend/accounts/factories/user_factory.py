import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "User %03d" % n)
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "muhome")
    is_private = False
