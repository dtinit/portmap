import factory
from django.contrib.auth.hashers import make_password
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token

from portmap.core.models import User

from .defaults import DEFAULT_PASSWORD


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = "test@example.com"
    password = make_password(DEFAULT_PASSWORD)


@register
class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        user = UserFactory()
        return manager.get_or_create(user=user)[0]
