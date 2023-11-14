from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):

    def __str__(self):
        return self.email


class Article(BaseModel):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    body = models.TextField()
    datatype = models.CharField(max_length=30)
    sources = models.TextField(max_length=500)
    destinations = models.TextField(max_length=500)

    @classmethod
    def datatypes(cls):
        return Article.objects.order_by("datatype").distinct("datatype")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        self.sources = Article._reformat_yaml_list(self.sources)
        self.destinations = Article._reformat_yaml_list(self.destinations)

    @classmethod
    def _reformat_yaml_list(cls, the_list):
        return ','.join([item.strip(" '") for item in the_list.strip('[]').split(',')])

    def source_list(self):
        return self.sources.split(',')

    def destination_list(self):
        return self.destinations.split(',')
