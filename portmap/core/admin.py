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
    list_display = ("name", "datatype", "title", "source_list", "destination_list", "view_count", )

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

@register(TrackArticleView, site=admin_site)
class TestingArticleViewAdmin(admin.ModelAdmin):
    list_display = ("article", "article_path", "visited_directly", "external_referrer", )
