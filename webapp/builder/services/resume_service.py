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
        posted_resume_jobs = ResumeJobsFormset(payload, prefix='resume_job')
        posted_education_forms = ResumeEducationFormset(payload, prefix='resume_education')
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

        #     if posted_resume_jobs.is_valid():  
        #         for form in posted_resume_jobs:
        #             if form.has_changed():
        #                 resume_job = form.save(commit=False)
        #                 if resume_job.resume is None:
        #                     resume_job.resume = resume
        #                 resume_job.save()
                
        #     if posted_education_forms.is_valid():
        #         for form in posted_education_forms:
        #             if form.has_changed():
        #                 resume_education = form.save(commit=False)
        #                 if resume_education.resume is None:
        #                     resume_education.resume = resume
        #                 resume_education.save()
        #     resume.save()
        #     return True
        # except Exception as ex:
        #     return False           
        # return False
    
    def save_resume_details(self, resume, payload):
        posted_resume_details = ResumeDetailsForm(payload)
        if posted_resume_details.is_valid():
            form = posted_resume_details
            resume.resume_title=form.cleaned_data.get('resume_title')
            resume.contact_information_section_title=form.cleaned_data.get('contact_information_section_title')
            resume.contact_information=form.cleaned_data.get('contact_information')
            resume.personal_statement_section_title=form.cleaned_data.get('personal_statement_section_title')
            resume.personal_statement=form.cleaned_data.get('personal_statement')
            resume.current_skills_section_title=form.cleaned_data.get('current_skills_section_title')
            resume.current_skills=form.cleaned_data.get('current_skills')
            return None
        else:
            return form

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
