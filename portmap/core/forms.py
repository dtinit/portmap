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
    data_type_choices = (('error', 'data missing'))
    datatype = forms.ChoiceField(label="Data/Content Type", choices=data_type_choices)
    datasource = forms.ChoiceField(label="Where the data is currently", choices=(()))
    datadest = forms.ChoiceField(label="Destination", choices=(()))

    def __init__(self, data, datatypes=None):
        super().__init__(data=data)
        self.fields['datatype'].choices = [("", "Select an option")] + [(item, item) for item in datatypes]
        self.fields['datasource'].disabled = True
        self.fields['datadest'].disabled = True
