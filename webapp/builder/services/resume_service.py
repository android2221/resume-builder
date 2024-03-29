from builder.forms import ActivateResumeForm, ResumeJobsFormset, ResumeDetailsForm, ResumeEducationFormset, ResumeJobsSectionTitleForm, ResumeEducationSectionTitleForm
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from builder.models import Resume
import requests
from builder.models import ResumeJob, ResumeEducation

class ResumeService():

    def get_resume_by_profile_url(self, request_profile_url, is_draft):
        try:
            account = Account.objects.get(profile_url=request_profile_url)
            resume = self.get_resume_for_user(account.user.id, is_draft)
            draft_resume = self.get_resume_for_user(account.user.id, True)
            if draft_resume.is_live is True:
                return resume
        except ObjectDoesNotExist:
            return None
        return None

    def get_resume_for_user(self, user_id, is_draft=True):
        try:
            resume = Resume.objects.get(user_id=user_id, is_draft=is_draft)
        except ObjectDoesNotExist:
            resume = Resume(user_id=user_id, is_draft=is_draft)
            resume.save()
        return resume
    
    def get_resume_jobs_by_id(self, resume_id):
        return ResumeJob.objects.filter(resume=resume_id).order_by('resume_position')
    
    def get_resume_education_by_id(self, resume_id):
        return ResumeEducation.objects.filter(resume=resume_id).order_by('resume_position')

    def save_resume(self, resume, post_payload):
        try:
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
        except Exception as e:
            print(e)
            
    
    def publish_resume_for_user(self, user):
        draft_resume = self.get_resume_for_user(user.id, True)
        draft_jobs = draft_resume.resumejob_set.all()
        draft_education = draft_resume.resumeeducation_set.all()
        current_resume = self.get_resume_for_user(user.id, False)
        current_resume.delete()
        new_resume = draft_resume
        new_resume.is_draft = False
        new_resume.pk = None
        new_resume.save()
        for job in draft_jobs:
            job.pk = None
            job.resume = new_resume
            job.save()
        for education in draft_education:
            education.pk = None
            education.resume = new_resume
            education.save()

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
        draft_resume = self.get_resume_for_user(resume.user.id, True)
        resume_active_form = {'profile_active': draft_resume.is_live }
        return ActivateResumeForm(resume_active_form)

    def init_builder_forms(self, user_id):
        draft_resume = self.get_resume_for_user(user_id, True)
        live_resume = self.get_resume_for_user(user_id, False)

        return {
            'activate_profile_form': self.init_resume_active_form(live_resume),
            'resume_details_form': ResumeDetailsForm(self.init_resume_detail_form_data(draft_resume)),
            'resume_jobs_section_title_form': ResumeJobsSectionTitleForm(self.init_resume_jobs_section_title_form(draft_resume)),
            'resume_education_section_title_form': ResumeEducationSectionTitleForm(self.init_resume_education_section_title_form(draft_resume)),
            'resume_jobs_formset': ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=draft_resume.pk).order_by('resume_position'), prefix='resume_job'),
            'resume_education_formset': ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=draft_resume.pk).order_by('resume_position'), prefix='resume_education')
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
        forms = ResumeEducationFormset(post_payload, prefix='resume_education', queryset=ResumeEducation.objects.filter(resume=resume.pk))
        if forms.is_valid():
            forms.save(commit=False)
            for form in forms:
                if form.has_changed():
                    resume_education = form.save(commit=False)
                    resume_education.resume = resume
                    resume_education.resume_position = form.cleaned_data['ORDER']
                    resume_education.save()
            for obj in forms.deleted_objects:   
                obj.delete()
            return ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=resume.pk), prefix='resume_education')
        else:    
            return forms

    def process_resume_jobs_formset(self, post_payload, resume):
        forms = ResumeJobsFormset(post_payload, prefix='resume_job', queryset=ResumeJob.objects.filter(resume=resume.pk))
        if forms.is_valid():  
            forms.save(commit=False)
            for form in forms:
                if form.has_changed():
                    resume_job = form.save(commit=False)
                    resume_job.resume = resume
                    resume_job.resume_position = form.cleaned_data['ORDER']
                    resume_job.save()
            for obj in forms.deleted_objects:
                obj.delete()
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
                resume = self.get_resume_for_user(user.id, True)
                resume.is_live = form.cleaned_data["profile_active"]
                resume.save()
                return True
            except Exception:
                return False
