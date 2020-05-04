from builder.forms import ResumeEditorForm, ActivateResumeForm, ResumeJobsFormset, ResumeDetailsForm, ResumeEducationFormset
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from builder.models import ResumeJob, ResumeEducation
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
        jobs = ResumeJob.objects.filter(resume=request.user.resume.pk)
        profile_form_data = {'profile_active': request.user.resume.is_live }
        return {'activate_profile_form': ActivateResumeForm(profile_form_data),
            'resume_details_form': ResumeDetailsForm(),
            'resume_jobs_formset': ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=request.user.resume.pk), prefix='resume_job'),
            'resume_education_formset': ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=request.user.resume.pk), prefix='resume_education')
        }
    
    def save_resume(self, resume, payload):
        posted_resume_forms = ResumeJobsFormset(payload, prefix='resume_job')
        posted_education_forms = ResumeEducationFormset(payload, prefix='resume_education')
        print('save hit')
        # Save resume jobs
        try:
            if posted_resume_forms.is_valid():  
                print('jobs valid')          
                for form in posted_resume_forms:
                    if form.has_changed():
                        resume_job = form.save(commit=False)
                        resume_job.resume = resume
                        resume_job.save()
                        print(resume_job)
                
            if posted_education_forms.is_valid():
                print('education valid')          
                for form in posted_education_forms:
                    if form.has_changed():
                        resume_education = form.save(commit=False)
                        resume_education.resume = resume
                        resume_education.save()
                        print(resume_education)
            return True
        except Exception as ex:
            print(ex)
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
