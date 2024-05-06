import factory
from django.contrib.auth.hashers import make_password
from pytest_factoryboy import register

from portmap.core.models import User, Article

from tests.core.fixtures.defaults import DEFAULT_PASSWORD


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = "test@example.com"
    password = make_password(DEFAULT_PASSWORD)

@register
class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    name = factory.Faker('file_name', extension='md')
    datatype = factory.Faker('word')
    sources = factory.Faker('word')
    destinations = factory.Faker('word')
    title = factory.Faker('sentence')
    body = factory.Faker('paragraph')
