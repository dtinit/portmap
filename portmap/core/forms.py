from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.renderers import TemplatesSetting

from .models import User, UseCaseFeedback


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

class ArticleFeedbackForm(forms.Form):
    CHOICES = [('happy', '<span>yes</span>'),
               ('sad', '<span>no</span>')]
    reaction = forms.ChoiceField(label="Did this article help?", widget=forms.RadioSelect, choices=CHOICES)
    explanation = forms.CharField(widget=forms.Textarea,
                                  required=False,
                                  label="Please tell us about your use case or what would make this article better")

class UseCaseFeedbackForm(forms.ModelForm):
    class Meta:
        model = UseCaseFeedback
        fields = ['explanation', 'datatype', 'source', 'destination']
        labels = {
            "explanation": "If none of these solutions works for you, can you explain why?",
        }
        help_texts = {
            "explanation": "Information about use cases helps us understand what portability and other interop features would be most helpful"
        }
        widgets = {
            "explanation": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "datatype": forms.HiddenInput(),
            "source": forms.HiddenInput(),
            "destination": forms.HiddenInput()
        }

    def __init__(self, data, datatype=None, source=None, destination=None):
        super().__init__(data=data)
        if datatype:
            self.fields['datatype'].initial = datatype
        if source:
            self.fields['source'].initial = source
        if destination:
            self.fields['destination'].initial = destination
            # Populating the form with values we already know

