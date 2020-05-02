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
    
    def build_resume_forms(self, request):
        print(request.user.resume.pk)
        jobs = ResumeJob.objects.filter(resume=request.user.resume.pk)
        print(jobs)
        profile_form_data = {'profile_active': request.user.resume.is_live }
        return {'activate_profile_form': ActivateResumeForm(profile_form_data),
            'resume_jobs_formset': ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=request.user.resume.pk))
        }
    
    def save_resume(self, resume, payload):
        posted_resume_forms = ResumeJobsFormset(payload)
        if posted_resume_forms.is_valid():
            try:
                for form in posted_resume_forms:
                    resume_job = form.save(commit=False)
                    resume_job.resume = resume
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
