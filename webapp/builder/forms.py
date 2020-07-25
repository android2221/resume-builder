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
    def __init__(self, *args, **kwargs):
        super(ResumeJobsSectionTitleForm, self).__init__(*args, **kwargs)
        self.fields['resume_jobs_section_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 

class ResumeEducationSectionTitleForm(forms.Form):
    resume_education_section_title=forms.CharField(required=False)
    error_css_class='error'
    def __init__(self, *args, **kwargs):
        super(ResumeEducationSectionTitleForm, self).__init__(*args, **kwargs)
        self.fields['resume_education_section_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 

class ResumeDetailsForm(forms.Form):
    resume_title=forms.CharField(required=False)
    contact_information_section_title=forms.CharField(required=False)
    contact_information=forms.CharField(widget=forms.Textarea(), required=False)
    personal_statement_section_title=forms.CharField(required=False)
    personal_statement=forms.CharField(widget=forms.Textarea(), required=False)
    current_skills_section_title=forms.CharField(required=False)
    current_skills=forms.CharField(widget=forms.Textarea(), required=False)
    # # For testing error states
    # def clean(self):
    #     cd = self.cleaned_data
    #     self.add_error('resume_title', "ERRORS")
    #     return cd

    def __init__(self, *args, **kwargs):
        super(ResumeDetailsForm, self).__init__(*args, **kwargs)
        self.fields['resume_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 
        self.fields['contact_information_section_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 
        self.fields['contact_information'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 
        self.fields['personal_statement_section_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 
        self.fields['personal_statement'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 
        self.fields['current_skills_section_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME 
        self.fields['current_skills'].widget.attrs['class'] = constants.INPUT_STYLE_NAME

class ResumeJobFormsetForm(forms.ModelForm):
    class Meta:
        model = ResumeJob
        fields=('position_title', 'company_name', 'start_date', 'end_date', 'position_description')

    def __init__(self, *args, **kwargs):
        super(ResumeJobFormsetForm, self).__init__(*args, **kwargs)
        self.fields['position_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['company_name'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['start_date'].widget.attrs['class'] = constants.INPUT_STYLE_NAME + ' ' + 'datepicker'
        self.fields['start_date'].widget.attrs['readonly'] = "readonly"
        self.fields['end_date'].widget.attrs['class'] = constants.INPUT_STYLE_NAME + ' ' + 'datepicker'
        self.fields['end_date'].widget.attrs['readonly'] = "readonly"
        self.fields['position_description'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['position_title'].required = False
        self.fields['company_name'].required = False
        self.fields['position_description'].required = False

class ResumeEducationFormsetForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ResumeEducationFormsetForm, self).__init__(*args, **kwargs)
        self.fields['education_title'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['institution_name'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['start_date'].widget.attrs['class'] = constants.INPUT_STYLE_NAME + ' ' + 'datepicker'
        self.fields['start_date'].widget.attrs['readonly'] = "readonly"
        self.fields['end_date'].widget.attrs['class'] = constants.INPUT_STYLE_NAME + ' ' + 'datepicker'
        self.fields['end_date'].widget.attrs['readonly'] = "readonly"
        self.fields['education_description'].widget.attrs['class'] = constants.INPUT_STYLE_NAME

ResumeEducationFormset = modelformset_factory(
    ResumeEducation,
    fields=('education_title', 'institution_name', 'start_date', 'end_date', 'education_description'),
    form=ResumeEducationFormsetForm,
    validate_min=True,
    can_delete=True,
    can_order=True
)

ResumeJobsFormset = modelformset_factory(
    ResumeJob,
    form=ResumeJobFormsetForm,
    validate_min=True,
    can_delete=True,
    can_order=True
)
