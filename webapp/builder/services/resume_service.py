from builder.forms import ActivateResumeForm, ResumeJobsFormset, ResumeDetailsForm, ResumeEducationFormset, ResumeJobsSectionTitleForm, ResumeEducationSectionTitleForm
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from builder.models import Resume
import requests
from builder.models import ResumeJob, ResumeEducation

class ResumeService():

    def get_resume_by_profile_url(self, request_profile_url):
        try:
            account = Account.objects.get(profile_url=request_profile_url)
            resume = self.get_resume_for_user(account.user.id)
            if resume.is_live is True:
                return resume
        except ObjectDoesNotExist:
            return None
        return None

    def get_resume_for_user(self, user_id, is_draft=True):
        resume = Resume.objects.get(user=user_id, is_draft=is_draft)
        if not resume:
            resume = Resume(user=user_id, is_draft=is_draft)
            resume.save()
        else:
            return resume
    
    def get_resume_jobs_by_id(self, resume_id):
        return ResumeJob.objects.filter(resume=resume_id)
    
    def get_resume_education_by_id(self, resume_id):
        return ResumeEducation.objects.filter(resume=resume_id)

    def save_resume(self, resume, post_payload):
        resume_details_form = self.process_resume_detail_form(post_payload, resume)
        resume_jobs_formset = self.process_resume_jobs_formset(post_payload, resume)
        resume_education_formset = self.process_resume_education_formset(post_payload, resume)
        resume_jobs_section_title_form = self.process_resume_section_title_form(post_payload, resume)
        resume_education_section_title_form = self.process_resume_education_section_title_form(post_payload, resume)
        forms = {
            'resume_details_form': resume_details_form,
            'resume_jobs_formset': resume_jobs_formset,
            'resume_education_formset': resume_education_formset,
            'resume_jobs_section_title_form': resume_jobs_section_title_form,
            'resume_education_section_title_form': resume_education_section_title_form,
            'activate_profile_form': self.init_resume_active_form(resume)
        }
        resume.save()
        return forms

    def init_resume_detail_form_data(self, resume):
        return { 
            'resume_title': resume.resume_title,
            'contact_information_section_title': resume.contact_information_section_title,
            'contact_information': resume.contact_information,
            'personal_statement_section_title': resume.personal_statement_section_title,
            'personal_statement': resume.personal_statement,
            'current_skills_section_title': resume.current_skills_section_title,
            'current_skills': resume.current_skills
        }
    
    def init_resume_jobs_section_title_form(self, resume):
        return {'resume_jobs_section_title': resume.resume_jobs_section_title}
    
    def init_resume_education_section_title_form(self, resume):
        return {'resume_education_section_title': resume.resume_education_section_title}
    
    def init_resume_active_form(self, resume):
        resume_active_form = {'profile_active': resume.is_live }
        return ActivateResumeForm(resume_active_form)

    def init_forms_from_resume(self, resume):
        return {
            'activate_profile_form': self.init_resume_active_form(resume),
            'resume_details_form': ResumeDetailsForm(self.init_resume_detail_form_data(resume)),
            'resume_jobs_section_title_form': ResumeJobsSectionTitleForm(self.init_resume_jobs_section_title_form(resume)),
            'resume_education_section_title_form': ResumeEducationSectionTitleForm(self.init_resume_education_section_title_form(resume)),
            'resume_jobs_formset': ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=resume.pk), prefix='resume_job'),
            'resume_education_formset': ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=resume.pk), prefix='resume_education')
            }
        
    def process_resume_education_section_title_form(self, post_payload, resume):
        form = ResumeEducationSectionTitleForm(post_payload)
        if form.is_valid():
            resume.resume_education_section_title = form.cleaned_data.get('resume_education_section_title')
            return ResumeEducationSectionTitleForm(self.init_resume_education_section_title_form(resume))
        else:
            return form

    def process_resume_section_title_form(self, post_payload, resume):
        form = ResumeJobsSectionTitleForm(post_payload)
        if form.is_valid():
            resume.resume_jobs_section_title = form.cleaned_data.get('resume_jobs_section_title')
            return ResumeJobsSectionTitleForm(self.init_resume_jobs_section_title_form(resume))
        else:
            return form

    def process_resume_education_formset(self, post_payload, resume):
        forms = ResumeEducationFormset(post_payload, prefix='resume_education')
        if forms.is_valid():
            for form in forms:
                if form.has_changed():
                    resume_education = form.save(commit=False)
                    resume_education.resume = resume
                    resume_education.save()
            return ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=resume.pk), prefix='resume_education')
        else:    
            return forms

    def process_resume_jobs_formset(self, post_payload, resume):
        print('formset')
        forms = ResumeJobsFormset(post_payload, prefix='resume_job', queryset=resume.resumejob_set.all())
        print(forms.errors)
        if forms.is_valid():  
            for form in forms:
                print(resume.is_draft)
                if form.has_changed():
                    print('job saving')
                    resume_job = form.save(commit=False)
                    resume_job.resume = resume
                    resume_job.save()
            return ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=resume.pk), prefix='resume_job')
        else:
            return forms
        
    def process_resume_detail_form(self, post_payload, resume):
        form = ResumeDetailsForm(post_payload)
        if form.is_valid():
            resume.resume_title=form.cleaned_data.get('resume_title')
            resume.contact_information_section_title=form.cleaned_data.get('contact_information_section_title')
            resume.contact_information=form.cleaned_data.get('contact_information')
            resume.personal_statement_section_title=form.cleaned_data.get('personal_statement_section_title')
            resume.personal_statement=form.cleaned_data.get('personal_statement')
            resume.current_skills_section_title=form.cleaned_data.get('current_skills_section_title')
            resume.current_skills=form.cleaned_data.get('current_skills')
            resume.save()
            return ResumeDetailsForm(self.init_resume_detail_form_data(resume))
        else:
            return form

    def toggle_resume_active(self, user, payload):
        form = ActivateResumeForm(payload)
        if form.is_valid():
            try:
                resume = self.get_resume_for_user(user.id)
                resume.is_live = form.cleaned_data["profile_active"]
                resume.save()
                return True
            except Exception as e:
                print(e)
                return False
