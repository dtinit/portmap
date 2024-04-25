from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin

from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.db import connection
from django.db.models import Count

from .forms import UserChangeForm, UserCreationForm
from .models import User, Article, Feedback, QueryLog, UseCaseFeedback, DataType, TrackArticleView
from .articles import get_content_files

class PortmapAdminSite(admin.AdminSite):
    site_header = "Portmap Admin"

    class Meta:
        pass


admin_site = PortmapAdminSite(name="portmap_admin")
admin_site._registry.update(admin.site._registry)


@register(Article, site=admin_site)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "datatype", "title", "source_list", "destination_list")

    def get_urls(self):
        urls = super().get_urls()
        urls = [path("populate/", self.admin_site.admin_view(self.populate)),
                *urls]
        return urls

    def populate(self, request):
        get_content_files()
        return HttpResponse("Done")

@register(Feedback, site=admin_site)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "created_at", "reaction", "explanation")


@register(QueryLog, site=admin_site)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "datatype", "source", "destination")

@register(UseCaseFeedback, site=admin_site)
class UseCaseFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'datatype', 'source', 'destination', 'explanation' )

@register(User, site=admin_site)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ["email", "username"]
    readonly_fields = [
        "date_joined",
        "last_login",
    ]

@register(DataType, site=admin_site)
class DataTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'helpText')

@register(TrackArticleView, site=admin_site)
class TrackArticleViewAdmin(admin.ModelAdmin):
    list_display = ('article_path', "count", "visited_directly", "external_referrer",)
    aggregated_counts = {}

    def count(self, object):
        matched_item = next(item for item in self.aggregated_counts if item["article_path"] == object.article_path)
        return matched_item["count"]

    def get_queryset(self, request):
        qs = super(TrackArticleViewAdmin, self).get_queryset(request)
        self.aggregated_counts = list(qs.values("article_path").annotate(count=Count('article_path')))
        return qs.annotate(count=Count('article_path'))

    def get_object(self, request, object_id, from_field=None):
        return TrackArticleView.objects.filter(id=object_id).first()
