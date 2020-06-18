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

class ResumeJobsSectionTitleForm(forms.Form):
    resume_jobs_section_title=forms.CharField(required=False)
    error_css_class='error'

class ResumeEducationSectionTitleForm(forms.Form):
    resume_education_section_title=forms.CharField(required=False)
    error_css_class='error'

class ResumeDetailsForm(forms.Form):
    resume_title=forms.CharField(required=False)
    contact_information_section_title=forms.CharField(required=False)
    contact_information=forms.CharField(widget=forms.Textarea(), required=False)
    personal_statement_section_title=forms.CharField(required=False)
    personal_statement=forms.CharField(widget=forms.Textarea(), required=False)
    current_skills_section_title=forms.CharField(required=False)
    current_skills=forms.CharField(widget=forms.Textarea(), required=False)

class ResumeJobFormsetForm(forms.ModelForm):
    class Meta:
        model = ResumeJob
        fields=('position_title', 'company_name', 'start_date', 'end_date', 'position_description')

    def __init__(self, *args, **kwargs):
        super(ResumeJobFormsetForm, self).__init__(*args, **kwargs)
        self.fields['position_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['company_name'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['start_date'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['end_date'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['position_description'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['position_title'].widget.attrs['placeholder'] = constants.RESUME_JOB_TITLE_PLACEHOLDER
        self.fields['company_name'].widget.attrs['placeholder'] = constants.RESUME_JOB_COMPANY_NAME
        self.fields['start_date'].widget.attrs['placeholder'] = constants.RESUME_JOB_START_DATE
        self.fields['end_date'].widget.attrs['placeholder'] = constants.RESUME_JOB_END_DATE
        self.fields['position_description'].widget.attrs['placeholder'] = constants.RESUME_JOB_POSITION_DESCRIPTION

class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        exclude = ()

ResumeEducationFormset = modelformset_factory(
    ResumeEducation,
    fields=('education_title', 'institution_name', 'start_date', 'end_date', 'education_description'),
    form=ResumeEducationForm,
    validate_min=True
)

ResumeJobsFormset = modelformset_factory(
    ResumeJob,
    form=ResumeJobFormsetForm,
    validate_min=True
)
