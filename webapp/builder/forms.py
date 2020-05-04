from accounts import constants
from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from .models import ResumeJob, Resume, ResumeEducation

class ActivateResumeForm (forms.Form):
    profile_active = forms.BooleanField(required=False, label="", widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ActivateResumeForm, self).__init__(*args, **kwargs)
        self.fields["profile_active"].widget.attrs={'id': "activate-profile-checkbox"}

class ResumeDetailsForm(forms.Form):
    resume_title=forms.CharField()
    contact_information=forms.CharField(widget=forms.Textarea(), required=False)
    personal_statement=forms.CharField(widget=forms.Textarea(), required=False)
    current_skills=forms.CharField(widget=forms.Textarea(), required=False)

class ResumeJobFormsetForm(forms.ModelForm):
    class Meta:
        model = ResumeJob
        exclude = ()

class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        exclude = ()

ResumeEducationFormset = modelformset_factory(
    ResumeEducation,
    fields=('education_title', 'institution_name', 'start_date', 'end_date', 'degree_year', 'education_description'),
    form=ResumeEducationForm,
    validate_min=True
)

ResumeJobsFormset = modelformset_factory(
    ResumeJob,
    fields=('position_title', 'company_name', 'start_date', 'end_date', 'position_description'),
    form=ResumeJobFormsetForm,
    validate_min=True
)
