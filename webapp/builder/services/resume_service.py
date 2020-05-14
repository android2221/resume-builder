from builder.forms import ActivateResumeForm, ResumeJobsFormset, ResumeDetailsForm, ResumeEducationFormset, ResumeJobsSectionTitleForm, ResumeEducationSectionTitleForm
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from builder.models import ResumeJob, ResumeEducation
import requests

class ResumeService():

    def get_resume_by_profile_url(self, request_profile_url):
        try:
            accounts = Account.objects.filter(profile_url=request_profile_url)
            account = Account.objects.get(profile_url=request_profile_url)
            if account.user.resume.is_live is True:
                return account.user.resume
        except ObjectDoesNotExist:
            return None
        return None
    
    def get_resume_jobs_by_id(self, resume_id):
        return ResumeJob.objects.filter(resume=resume_id)
    
    def get_resume_education_by_id(self, resume_id):
        return ResumeEducation.objects.filter(resume=resume_id)

    def save_resume(self, resume, payload):
        posted_resume_jobs_section_title_form = ResumeJobsSectionTitleForm(payload)
        posted_resume_education_section_title_form = ResumeEducationSectionTitleForm(payload)
        try:
            resume_details_result = self.save_resume_details(resume, payload)
            save_results = {
                "resume_details_result": resume_details_result
            }
            resume.save()
        except Exception as ex:
            return False
        return save_results

        #     if posted_resume_jobs_section_title_form.is_valid():
        #         form = posted_resume_jobs_section_title_form
        #         resume.resume_jobs_section_title = form.cleaned_data.get('resume_jobs_section_title')

        #     if posted_resume_education_section_title_form.is_valid():
        #         form = posted_resume_education_section_title_form
        #         resume.resume_education_section_title = form.cleaned_data.get('resume_education_section_title')
                
        #     resume.save()
        #     return True
        # except Exception as ex:
        #     return False           
        # return False

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
