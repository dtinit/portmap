from functools import wraps
import json
import markdown
from allauth.account.views import LoginView as AllAuthLoginView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe

from .forms import UpdateAccountForm, QueryIndexForm, ArticleFeedbackForm, UseCaseFeedbackForm
from .models import User, Article, Feedback, QueryLog, UseCaseFeedback


def ux_requires_post(function):
    @wraps(function)
    def _wrap_requires_post(request, *args, **kwargs):
        if request.method == "POST":
            return function(request, *args, **kwargs)
        messages.success(request, "Page not GETtable, returning home")
        return redirect("index")
    return _wrap_requires_post

def index(request):
    query_structure = Article.get_query_structure()
    form = QueryIndexForm(data=None, datatypes=query_structure.keys())
    return TemplateResponse(request,
                            "core/index.html",
                            {'form': form, 'query_structure': json.dumps(query_structure)})


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
    html = mark_safe(markdown.markdown(article.body))
    context = {'article': article,
               'article_body_html': html,
               'article_name': article_name,
               'reaction_form': ArticleFeedbackForm()}
    return TemplateResponse(request, "core/article.html", context)


def find_articles(request):
    datatypes = Article.datatypes()
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = QueryIndexForm(data=request.POST, datatypes=datatypes)
        if form['datatype']:
            possible_articles = Article.objects.filter(datatype__contains=form.data['datatype'],
                                                       sources__contains=form.data['datasource'],
                                                       destinations__contains=form.data['datadest'])
            QueryLog.objects.create(datatype=form.data['datatype'],
                                    source=form.data['datasource'],
                                    destination=form.data['datadest'])
            if possible_articles.count() == 1:
                return redirect(f"/articles/{possible_articles[0].name}", )
            else:
                use_case_feedback= UseCaseFeedbackForm(data=None,
                                                       datatype=form.data['datatype'],
                                                       source=form.data['datasource'],
                                                       destination=form.data['datadest'])
                context = {'articles': possible_articles, 'usecase_form': use_case_feedback}
                return TemplateResponse(request, "core/article_list.html", context)

    else:
        form = QueryIndexForm(data=None, datatypes=datatypes)
        return TemplateResponse(request, "core/index.html", {'form': form, 'datatypes': datatypes})


@ux_requires_post
def article_feedback(request, article_name):
    form = ArticleFeedbackForm(data=request.POST)
    Feedback.objects.create(article=Article.objects.get(name=article_name),
                            reaction=form.data['reaction'],
                            explanation=form.data['explanation'])
    return TemplateResponse(request, "core/thankyou.html")


@ux_requires_post
def usecase_feedback(request):
    UseCaseFeedbackForm(data=request.POST).save()
    return TemplateResponse(request, "core/thankyou.html")


def debug_list_articles(request):
    if not settings.DEBUG:
        raise Http404
    articles = Article.objects.all()
    return TemplateResponse(request, "core/debug_article_list.html", {"articles": articles})


def debug_help_dev(request):
    return TemplateResponse(request, "core/debug_index.html")
