from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.renderers import TemplatesSetting
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomFormRenderer(TemplatesSetting):
    form_template_name = "forms/custom.html"


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username")


class UpdateAccountForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = User
        fields = ("first_name", "last_name")

class QueryIndexForm(forms.Form):
    content_type_choices = (('error', 'data missing'))
    content_type = forms.ChoiceField(label="Content Type", choices=content_type_choices)

    def __init__(self, data, datatypes=None):
        super().__init__(data=data)
        self.fields['content_type'].choices = [(item, item) for item in datatypes]
