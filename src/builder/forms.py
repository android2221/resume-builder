from django import forms
from django.contrib.auth.models import User
from mdeditor.fields import MDTextFormField

class ResumeEditorForm (forms.Form):
    content = MDTextFormField (label="")

class ActivateResumeForm (forms.Form):
    profile_active = forms.BooleanField(required=False, label="")

    def __init__(self, *args, **kwargs):
        super(ActivateResumeForm, self).__init__(*args, **kwargs)
        self.fields["profile_active"].widget.attrs={'class': "activate-profile"}
