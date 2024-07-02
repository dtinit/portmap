from functools import wraps
import json
import markdown2
import pycmarkgfm
from allauth.account.views import LoginView as AllAuthLoginView
from django.utils.feedgenerator import DefaultFeed
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_control
from django.middleware.csrf import get_token
from .forms import UpdateAccountForm, QueryIndexForm, ArticleFeedbackForm, UseCaseFeedbackForm
from .models import User, Article, Feedback, QueryLog, UseCaseFeedback, DataType
from portmap.slack import notify
from .track import track_view

# Specify lucide icon names for each datatype.
# If there's no match, FALLBACK will be used.
# New datatypes should have icons added.
datatype_icon_map = {
    'Book History': 'library-big',
    'Contacts': 'contact',
    'Newsletter': 'send',
    'Notes': 'notebook-pen',
    'Photos': 'images',
    'Playlists': 'list-music',
    'Tasks': 'list-checks',
    'Text Social Media': 'message-square-heart',
    'Videos': 'video',
    'Viewing History': 'tv-minimal-play',
    'FALLBACK': 'file'
}

def ux_requires_post(function):
    @wraps(function)
    def _wrap_requires_post(request, *args, **kwargs):
        if request.method == "POST":
            return function(request, *args, **kwargs)
        messages.success(request, "Page not GETtable, returning home")
        return redirect("index")
    return _wrap_requires_post

@cache_control(max_age=24 * 60 * 60, public=True) # Allow caching for 24 hours (in seconds)
def index(request):
    return TemplateResponse(request, "core/index.html", _get_index_context())

def render_index_to_string():
    return render_to_string("core/index.html", _get_index_context())

def _get_index_context():
    query_structure = Article.get_query_structure()
    query_form = QueryIndexForm(data=None, datatypes=query_structure.keys())
    feedback_form = UseCaseFeedbackForm(data=None, datatype='None', source='', destination='')

    def create_datatype(datatype_object):
        name = datatype_object.name
        return {
            'id': '_'.join(name.split()),
            'name': name,
            'help': datatype_object.helpText,
            'icon': datatype_icon_map[name] if name in datatype_icon_map else datatype_icon_map['FALLBACK']
        }

    # Only map the datatypes that actually have articles
    datatypes = map(create_datatype, DataType.objects.filter(name__in=query_structure.keys()))

    return {'form': query_form,
               'query_structure': json.dumps(query_structure),
               'use_case_form': feedback_form,
                'datatypes': datatypes
            }

def csrf_token(request):
    if request.method != 'GET':
        raise HttpResponse(status=405)

    return JsonResponse({'csrf_token': get_token(request)})

@cache_control(max_age=24 * 60 * 60, public=True) # Allow caching for 24 hours (in seconds)
def about(request):
    return TemplateResponse(request, "core/about.html")

@login_required
def user_settings(request):
    form = UpdateAccountForm(instance=request.user)

    if request.method == "POST":
        form = UpdateAccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Account details have been updated!"))

    return TemplateResponse(request, "core/settings.html", {"form": form})

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
    return redirect("index")

class LoginView(AllAuthLoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if settings.DEBUG:
            context["all_users"] = User.objects.all()

        return context


def login_as_user(request):
    if not settings.DEBUG or request.method != "POST":
        raise Http404

    from django.contrib.auth import login

    as_user = User.objects.get(pk=int(request.POST.get("select_user")))
    backend = settings.AUTHENTICATION_BACKENDS[0]

    login(request, as_user, backend)

    messages.success(request, _("Successfully signed in as ") + str(as_user))
    return redirect("index")


def display_article(request, article_name):
    article = Article.objects.get(name=article_name)
    html = mark_safe(pycmarkgfm.gfm_to_html(article.body))
    context = {'article': article,
               'article_body_html': html,
               'article_name': article_name,
               'reaction_form': ArticleFeedbackForm()}
    track_view(request, article)
    return TemplateResponse(request, "core/article.html", context, headers={'cache-control':'no-store'})


def find_articles(request):
    datatypes = Article.datatypes()
    if request.method == "GET":
        # create a form instance and populate it with data from the request:
        form = QueryIndexForm(data=request.GET, datatypes=datatypes)

        if form['datatype']:

            # If a datatype wasn't specified, show a list of every article
            if not form.data.get('datatype'):
                context = {
                    'articles': Article.objects.order_by("title").all(),
                    'title': 'All articles',
                    'use_case_form': UseCaseFeedbackForm(data=None, datatype='None', source='', destination='')
                }
                return TemplateResponse(request, "core/article_list.html", context, headers={'cache-control':'no-store'})
            datatype_joined = " ".join(form.data['datatype'].split("_"))
            possible_articles = Article.objects.filter(datatype__contains=datatype_joined,
                                                       sources__contains=form.data['datasource'],
                                                       destinations__contains=form.data['datadest'])

            QueryLog.objects.create(datatype=form.data['datatype'],
                                    source=form.data['datasource'],
                                    destination=form.data['datadest'])

            message = "*New query:* Transfer " + form.data['datatype'] + " from " + form.data['datasource']
            if form.data['datadest']:
                message += " to " + form.data['datadest']

            notify(message)


            if possible_articles.count() == 1:
                return redirect(f"/articles/{possible_articles[0].name}")
            else:
                use_case_feedback= UseCaseFeedbackForm(data=None,
                                                       datatype=form.data['datatype'],
                                                       source=form.data['datasource'],
                                                       destination=form.data['datadest'])
                context = {'articles': possible_articles, 'use_case_form': use_case_feedback}
                return TemplateResponse(request, "core/article_list.html", context, headers={'cache-control':'no-store'})

    else:
        form = QueryIndexForm(data=None, datatypes=datatypes)
        return TemplateResponse(request, "core/index.html", {'form': form, 'datatypes': datatypes})


@ux_requires_post
def article_feedback(request, article_name):
    form = ArticleFeedbackForm(data=request.POST)
    Feedback.objects.create(article=Article.objects.get(name=article_name),
                            reaction=form.data['reaction'],
                            explanation=form.data['explanation'])
    message = "*New article feedback for \"" + article_name + "\"*:\n\nReaction: " + form.data['reaction'] + "\n\n" + form.data['explanation']
    notify(message)
    referer = request.META.get('HTTP_REFERER', '/')
    return TemplateResponse(request, "core/thankyou.html", {'referer': referer})


@ux_requires_post
def usecase_feedback(request):
    feedback = UseCaseFeedbackForm(data=request.POST);
    if feedback.is_valid():
        feedback.save()
        message = "*New use case feedback:*\n\n" + feedback.data['explanation']
        notify(message)

    referer = request.META.get('HTTP_REFERER', '/')
    return TemplateResponse(request, "core/thankyou.html", {'referer': referer})


def debug_list_articles(request):
    if not settings.DEBUG:
        raise Http404
    articles = Article.objects.all()
    return TemplateResponse(request, "core/debug_article_list.html", {"articles": articles})


def debug_help_dev(request):
    return TemplateResponse(request, "core/debug_index.html")

class CorrectMimeTypeFeed(DefaultFeed):
    content_type = 'application/xml; charset=utf-8'

class RssFeed(Feed):
    feed_type = CorrectMimeTypeFeed
    title_template = "feeds/article_title.html"
    description_template = "feeds/article_description.html"
    title = "RSS Feed"
    link = "https://portmap.dtinit.org/articles_feed"
    portmap_link = "https://portmap.dtinit.org"
    description = "Articles from Portability Articles repo"

    def items(self):
        parsed_articles = []

        for article in Article.objects.all():
            title = article.title
            body = article.body
            html_body = markdown2.markdown(body)
            html_url = article.get_absolute_url()
            created_at = article.created_at
            updated_at = article.updated_at

            parsed_articles.append({
                "title": title,
                "body": html_body,
                "html_url": html_url,
                "created_at": created_at,
                "updated_at": updated_at
            })

        return parsed_articles

    def item_link(self, item):
        return self.portmap_link + item["html_url"]

    def item_pubdate(self, item):
        return item["created_at"]

    def item_updateddate(self, item):
        return item["updated_at"]
