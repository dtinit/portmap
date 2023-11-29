from django.conf import settings
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.urls import path

from .forms import UserChangeForm, UserCreationForm
from .models import User, Article
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


CustomUserAdmin.fieldsets += (
    (
        "Sign up details",
        {"fields": ("terms_accepted_at", "marketing_list_accepted_at")},
    ),
)

