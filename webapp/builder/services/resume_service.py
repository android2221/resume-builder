from builder.forms import ResumeEditorForm, ActivateResumeForm, ResumeJobsFormset
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from builder.models import ResumeJob
import requests


class ResumeService():

    def get_rendered_resume_content(self, request_profile_url):
        try:
            account = Account.objects.get(profile_url=request_profile_url)
        except ObjectDoesNotExist:
            return None
        if account.user.resume.is_live is True:
            return account.user.resume.content
        return None
    
    def build_resume_forms(self, resume):
        profile_form_data = {'profile_active': resume.is_live }
        return {'activate_profile_form': ActivateResumeForm(profile_form_data),
            'resume_jobs_formset': ResumeJobsFormset() 
        }
    
    def save_resume(self, resume, payload):
        posted_forms = ResumeJobsFormset(payload)
        if posted_forms.is_valid():
            try:
                for form in posted_forms:
                    resume_job = ResumeJob()
                    resume_job.resume = resume
                    resume_job.position_title = form.cleaned_data.get('position_title')
                    resume_job.company_name = form.cleaned_data.get('company_name')
                    resume_job.start_date = form.cleaned_data.get('start_date')
                    resume_job.end_date = form.cleaned_data.get('end_date')
                    resume_job.position_description = form.cleaned_data.get('position_description')
                    resume_job.save()
                    resume.save()
                    return True
            except:
                return False           
            return False
    
    def preview_resume(self, payload):
        posted_form = ResumeEditorForm(payload)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            resume_content = form_data["content"]
            return resume_content
        return None

    def toggle_resume_active(self, user, payload):
        form = ActivateResumeForm(payload)
        if form.is_valid():
            try:
                user.resume.is_live = form.cleaned_data["profile_active"]
                user.resume.save()
                return True
            except:
                return False
