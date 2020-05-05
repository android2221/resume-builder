from builder.forms import ActivateResumeForm, ResumeJobsFormset, ResumeDetailsForm, ResumeEducationFormset, ResumeJobsSectionTitleForm, ResumeEducationSectionTitleForm
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from builder.models import ResumeJob, ResumeEducation
import requests

class ResumeService():

    def get_resume_by_profile_url(self, request_profile_url):
        try:
            account = Account.objects.get(profile_url=request_profile_url)
        except ObjectDoesNotExist:
            return None
        if account.user.resume.is_live is True:
            return account.user.resume
        return None
    
    def get_resume_jobs_by_id(self, resume_id):
        return ResumeJob.objects.filter(resume=resume_id)
    
    def get_resume_education_by_id(self, resume_id):
        return ResumeEducation.objects.filter(resume=resume_id)
    
    def build_resume_forms(self, request):
        jobs = ResumeJob.objects.filter(resume=request.user.resume.pk)
        profile_form_data = {'profile_active': request.user.resume.is_live }
        resume_jobs_section_title_form_data = {'resume_jobs_section_title': request.user.resume.resume_jobs_section_title}
        resume_education_section_title_form_data = {'resume_education_section_title': request.user.resume.resume_education_section_title}
        resume_detail_form_data = { 
            'resume_title': request.user.resume.resume_title,
            'contact_information_section_title': request.user.resume.contact_information_section_title,
            'contact_information': request.user.resume.contact_information,
            'personal_statement_section_title': request.user.resume.personal_statement_section_title,
            'personal_statement': request.user.resume.personal_statement,
            'current_skills_section_title': request.user.resume.current_skills_section_title,
            'current_skills': request.user.resume.current_skills
        }
        return {
            'activate_profile_form': ActivateResumeForm(profile_form_data),
            'resume_details_form': ResumeDetailsForm(resume_detail_form_data),
            'resume_jobs_section_title_form': ResumeJobsSectionTitleForm(resume_jobs_section_title_form_data),
            'resume_education_section_title_form': ResumeEducationSectionTitleForm(resume_education_section_title_form_data),
            'resume_jobs_formset': ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=request.user.resume.pk), prefix='resume_job'),
            'resume_education_formset': ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=request.user.resume.pk), prefix='resume_education')
        }
    
    def save_resume(self, resume, payload):
        posted_resume_details = ResumeDetailsForm(payload)
        posted_resume_jobs_section_title_form = ResumeJobsSectionTitleForm(payload)
        posted_resume_education_section_title_form = ResumeEducationSectionTitleForm(payload)
        posted_resume_jobs = ResumeJobsFormset(payload, prefix='resume_job')
        posted_education_forms = ResumeEducationFormset(payload, prefix='resume_education')
        # Save resume jobs
        try:
            if posted_resume_details.is_valid():
                form = posted_resume_details
                resume.resume_title=form.cleaned_data.get('resume_title')
                resume.contact_information_section_title=form.cleaned_data.get('contact_information_section_title')
                print(resume.contact_information_section_title)
                resume.contact_information=form.cleaned_data.get('contact_information')
                resume.personal_statement_section_title=form.cleaned_data.get('personal_statement_section_title')
                resume.personal_statement=form.cleaned_data.get('personal_statement')
                resume.current_skills_section_title=form.cleaned_data.get('current_skills_section_title')
                resume.current_skills=form.cleaned_data.get('current_skills')

            if posted_resume_jobs_section_title_form.is_valid():
                form = posted_resume_jobs_section_title_form
                resume.resume_jobs_section_title = form.cleaned_data.get('resume_jobs_section_title')

            if posted_resume_education_section_title_form.is_valid():
                form = posted_resume_education_section_title_form
                resume.resume_education_section_title = form.cleaned_data.get('resume_education_section_title')

            if posted_resume_jobs.is_valid():  
                for form in posted_resume_jobs:
                    if form.has_changed():
                        resume_job = form.save(commit=False)
                        if resume_job.resume is None:
                            resume_job.resume = resume
                        resume_job.save()
                
            if posted_education_forms.is_valid():
                for form in posted_education_forms:
                    if form.has_changed():
                        resume_education = form.save(commit=False)
                        if resume_education.resume is None:
                            resume_education.resume = resume
                        resume_education.save()
            resume.save()
            return True
        except Exception as ex:
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
