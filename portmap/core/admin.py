import json
import textwrap

from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.utils.html import format_html

from .forms import UserChangeForm, UserCreationForm
from .models import User, Article, Feedback, QueryLog, UseCaseFeedback, TrackArticleView
from .articles import get_content_files

class PortmapAdminSite(admin.AdminSite):
    site_header = "Portmap Admin"

    class Meta:
        pass

    def get_urls(self):
        urls = super().get_urls()
        urls = [path("analytics", analytics), *urls]
        return urls

admin_site = PortmapAdminSite(name="portmap_admin")
admin_site._registry.update(admin.site._registry)

@register(Article, site=admin_site)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "datatype", "title", "source_list", "destination_list", "view_count", )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _view_count=Count("trackarticleview", distinct=True),
        )
        return queryset

    def view_count(self, obj):
        return obj._view_count

    view_count.admin_order_field = '_view_count'

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
    readonly_fields = ("article_title", "article_link")
    list_display = ("id", "article", "article_title", "created_at", "reaction", "explanation")
    fieldsets = (
        ('', {
            'fields': (("article", "article_link"),
                       ("reaction", ),
                       ("explanation",))
        }),
    )

    def article_title(self, obj):
        return obj.article.title

    def article_link(self, obj):
        url = reverse(f"admin:core_article_change", args=(obj.article.pk,))
        return format_html(f"<a href='{url}''>{obj.article.title}</a>")


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
class TrackArticleViewAdmin(admin.ModelAdmin):
    list_display = ("article", "article_path", "visited_directly", "external_referrer", )

@staff_member_required
def analytics(request):
    datatype_interest_counts = {}
    datatype_provider_query_counts = {}

    for article in Article.objects.all():
        if article.datatype not in datatype_interest_counts:
            datatype_interest_counts[article.datatype] = {
                'views': 0,
                'queries': 0
            }

    for query in QueryLog.objects.all():
        # Query logs have datatypes stored
        # with underscores instead of spaces
        datatype_name = " ".join(query.datatype.split("_"))
        if datatype_name in datatype_interest_counts:
             datatype_interest_counts[datatype_name]['queries'] += 1

        if datatype_name not in datatype_provider_query_counts:
            datatype_provider_query_counts[datatype_name] = {
                'sources': {},
                'destinations': {},
                'transitions': {}
            }
        if query.source in datatype_provider_query_counts[datatype_name]['sources']:
            datatype_provider_query_counts[datatype_name]['sources'][query.source] += 1;
        else:
            datatype_provider_query_counts[datatype_name]['sources'][query.source] = 1;

        destination = query.destination if query.destination else 'None selected'
        if destination in datatype_provider_query_counts[datatype_name]['destinations']:
            datatype_provider_query_counts[datatype_name]['destinations'][destination] += 1;
        else:
            datatype_provider_query_counts[datatype_name]['destinations'][destination] = 1;

        transition = query.source + ' -> ' + destination

        if transition in datatype_provider_query_counts[datatype_name]['transitions']:
            datatype_provider_query_counts[datatype_name]['transitions'][transition] += 1
        else:
            datatype_provider_query_counts[datatype_name]['transitions'][transition] = 1

    for view in TrackArticleView.objects.select_related("article").all():
        datatype_interest_counts[view.article.datatype]['views'] += 1


    sentiment_query = Article.objects.annotate(happy_count=Count("feedback", filter=Q(feedback__reaction='happy')),
                                               sad_count = Count("feedback", filter=Q(feedback__reaction='sad')))
    article_sentiment = [{'name': article.name,
                          'title': textwrap.shorten(article.title, width=50),
                          'happy_count': range(article.happy_count),
                          'sad_count': range(article.sad_count)} for article in sentiment_query.order_by('-sad_count')]


    stats = json.dumps({
        'datatypeInterest': datatype_interest_counts,
        'providerQueriesByDatatype': datatype_provider_query_counts
    })

    return TemplateResponse(request, "admin/analytics.html", {'stats': stats, 'article_sentiment': article_sentiment})
