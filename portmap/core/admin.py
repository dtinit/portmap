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

    for datatype in Article.datatypes().values_list('datatype', flat=True):
        datatype_interest_counts[datatype] = {
            'views': 0,
            'queries': 0
        }

    # Process query logs
    for query in QueryLog.objects.iterator():
        datatype_name = " ".join(query.datatype.split("_"))
        if datatype_name in datatype_interest_counts:
            datatype_interest_counts[datatype_name]['queries'] += 1

            if datatype_name not in datatype_provider_query_counts:
                datatype_provider_query_counts[datatype_name] = {
                    'sources': {},
                    'destinations': {},
                    'transitions': {}
                }
            
            sources = datatype_provider_query_counts[datatype_name]['sources']
            sources[query.source] = sources.get(query.source, 0) + 1

            # Update destination counts
            destination = query.destination if query.destination else 'None selected'
            destinations = datatype_provider_query_counts[datatype_name]['destinations']
            destinations[destination] = destinations.get(destination, 0) + 1

            # Update transition counts
            transition = f"{query.source} -> {destination}"
            transitions = datatype_provider_query_counts[datatype_name]['transitions']
            transitions[transition] = transitions.get(transition, 0) + 1

    # Count views using database aggregation
    view_counts = (TrackArticleView.objects
                  .values('article__datatype')
                  .annotate(total=Count('id')))
    
    for vc in view_counts:
        datatype = vc['article__datatype']
        if datatype in datatype_interest_counts:
            datatype_interest_counts[datatype]['views'] = vc['total']

    sentiment_query = (Article.objects
                      .values('name', 'title')
                      .annotate(
                          happy_count=Count('feedback', filter=Q(feedback__reaction='happy')),
                          sad_count=Count('feedback', filter=Q(feedback__reaction='sad'))
                      )
                      .order_by('-sad_count'))

    article_sentiment = [{
        'name': article['name'],
        'title': textwrap.shorten(article['title'], width=50),
        'happy_count': range(article['happy_count']),
        'sad_count': range(article['sad_count'])
    } for article in sentiment_query]

    stats = json.dumps({
        'datatypeInterest': datatype_interest_counts,
        'providerQueriesByDatatype': datatype_provider_query_counts
    })

    return TemplateResponse(request, "admin/analytics.html", 
                          {'stats': stats, 'article_sentiment': article_sentiment})
