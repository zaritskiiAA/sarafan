import factory
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания фейк пользователей."""

    username = factory.Faker('name')

    class Meta:

        model = User
