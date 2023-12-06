from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.renderers import TemplatesSetting
from django.utils.safestring import mark_safe

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

class ReactionForm(forms.Form):
    choices = [('happy', '<span>yes</span>'),
               ('sad', '<span>no</span>')]
    reaction = forms.ChoiceField(label="Did this article help?", widget=forms.RadioSelect, choices=choices)
    explanation = forms.CharField(widget=forms.Textarea,
                                  required=False,
                                  label="Please tell us about your use case or what would make this article better")
