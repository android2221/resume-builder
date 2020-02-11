from accounts import constants
from django import forms
from django.contrib.auth.models import User

class ResumeEditorForm (forms.Form):
     content = forms.CharField(widget=forms.Textarea)

class ActivateResumeForm (forms.Form):
    profile_active = forms.BooleanField(required=False, label="")

    def __init__(self, *args, **kwargs):
        super(ActivateResumeForm, self).__init__(*args, **kwargs)
        self.fields["profile_active"].widget.attrs={'id': "activate-profile-checkbox"}
