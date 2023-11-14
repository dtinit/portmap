from allauth.account.views import LoginView as AllAuthLoginView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

from .forms import UpdateAccountForm, QueryIndexForm
from .models import User
from .articles import get_article, get_content_files

def index(request):
    articles = get_content_files()
    datatypes = set([article['datatype'] for article in articles])
    form = QueryIndexForm(data=None, datatypes=datatypes)
    return TemplateResponse(request, "core/index.html", {'form': form, 'datatypes':datatypes})

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
    article_content = get_article(article_name)
    # LMDTODO here is where we start to plug in the templating into HTML
    return HttpResponse(article_content)

def find_articles(request):
    articles = get_content_files()
    datatypes = set([article['datatype'] for article in articles])
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = QueryIndexForm(data=request.POST, datatypes=datatypes)
        if form.is_valid():
            possible_articles = [article for article in articles if form.data['content_type'] in article['datatype']]
            return TemplateResponse(request, "core/article_list.html", {'articles': possible_articles})

    else:
        form = QueryIndexForm(data=None, datatypes=datatypes)

    return TemplateResponse(request, "core/index.html", {'form': form, 'datatypes':datatypes})

def debug_list_articles(request):
    if not settings.DEBUG:
        raise Http404
    articles = get_content_files()
    return TemplateResponse(request, "core/debug_article_list.html", {"articles": articles})

def debug_help_dev(request):
    return TemplateResponse(request, "core/debug_index.html")
