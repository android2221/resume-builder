from accounts import constants
from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from .models import ResumeJob, Resume

class ResumeEditorForm (forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(ResumeEditorForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs={'class': "resume-editor"}

class ActivateResumeForm (forms.Form):
    profile_active = forms.BooleanField(required=False, label="", widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ActivateResumeForm, self).__init__(*args, **kwargs)
        self.fields["profile_active"].widget.attrs={'id': "activate-profile-checkbox"}

class ResumeDetailsForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('resume_title', 'personal_statement', 'current_skills')

class ResumeJobFormsetForm(forms.ModelForm):
    class Meta:
        model = ResumeJob
        exclude = ()

ResumeJobsFormset = modelformset_factory(
    ResumeJob,
    fields=('position_title', 'company_name', 'start_date', 'end_date', 'position_description'),
    extra=1,
    form=ResumeJobFormsetForm
)
