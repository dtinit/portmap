from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


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

admin.site.register(User, CustomUserAdmin)

admin_name = f"{settings.PROJECT_NAME} {_('Administration')}"
admin.site.site_title = admin_name
admin.site.site_header = admin_name
