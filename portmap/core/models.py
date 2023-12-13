from collections import defaultdict
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse


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

    @classmethod
    def get_query_structure(cls):
        structure = defaultdict(lambda: defaultdict(list))
        for article in Article.objects.all():
            datatype = article.datatype
            for source in article.source_list():
                for dest in article.destination_list():
                    if dest != source:
                        structure[datatype][source].append(dest)
        return structure

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        self.sources = Article._reformat_yaml_list(self.sources)
        self.destinations = Article._reformat_yaml_list(self.destinations)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Return the URL for the instance
        return reverse('display_article', args=[str(self.name)])

    @classmethod
    def _reformat_yaml_list(cls, the_list):
        return ','.join([item.strip(" '") for item in the_list.strip('[]').split(',')])

    def source_list(self):
        return self.sources.split(',')

    def destination_list(self):
        return self.destinations.split(',')

class Feedback(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    REACTION_CHOICES = [
        ('happy', 'happy'),
        ('sad', "sad"),
    ]
    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES,
        default='happy')
    explanation = models.TextField()

class UseCaseFeedback(BaseModel):
    datatype = models.CharField(max_length=30)
    source = models.TextField(max_length=100)
    destination = models.TextField(max_length=100)
    explanation = models.TextField()

class QueryLog(BaseModel):
    datatype = models.CharField(max_length=30)
    source = models.TextField(max_length=100)
    destination = models.TextField(max_length=100)
