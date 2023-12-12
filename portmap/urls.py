from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from .core import views
from .core.admin import admin_site

urlpatterns = [
    # admin
    path("dj-admin/", admin_site.urls),
    # accounts
    path("accounts/login/", views.LoginView.as_view(), name="account_login"),
    path("accounts/", include("allauth.urls")),
    path("accounts/settings/", views.user_settings, name="settings"),
    path("accounts/delete-account/", views.delete_account, name="delete_account"),
    # articles
    path("articles/<article_name>/feedback", views.article_feedback, name="article_feedback"),
    path('usecase_feedback', views.usecase_feedback, name='usecase_feedback'),
    path("articles/<article_name>/", views.display_article, name="display_article"),
    path("find_articles", views.find_articles, name="find_articles"),
    # core
    path("", views.index, name="index"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
        path("silk/", include("silk.urls", namespace="silk")),
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        ),
        path("login-as-user/", views.login_as_user, name="login_as_user"),
        path("__dev__/", views.debug_help_dev, name="debug_help_dev"),
        path("__dev__/list_articles/", views.debug_list_articles, name="debug_list_articles")
    ] + urlpatterns
