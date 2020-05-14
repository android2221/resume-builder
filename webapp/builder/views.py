from accounts import constants
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.conf import settings
from .services.resume_service import ResumeService
from django.contrib import messages
from builder.forms import ActivateResumeForm, ResumeJobsFormset, ResumeDetailsForm, ResumeEducationFormset, ResumeJobsSectionTitleForm, ResumeEducationSectionTitleForm
from builder.models import ResumeJob, ResumeEducation

def handler404(request, exception):
    response = render(request, "builder/404.html", {})
    response.status_code = 404
    return response


def index(request):
    return render(request, 'builder/index.html', {})


@login_required
def builder_page(request):
    service = ResumeService()
    forms = {}
    resume = request.user.resume
    # Variables
    resume_detail_form_data = { 
        'resume_title': request.user.resume.resume_title,
        'contact_information_section_title': request.user.resume.contact_information_section_title,
        'contact_information': request.user.resume.contact_information,
        'personal_statement_section_title': request.user.resume.personal_statement_section_title,
        'personal_statement': request.user.resume.personal_statement,
        'current_skills_section_title': request.user.resume.current_skills_section_title,
        'current_skills': request.user.resume.current_skills
    }
    if request.POST:
        # Get forms from POST
        posted_resume_details = ResumeDetailsForm(request.POST)
        posted_resume_jobs = ResumeJobsFormset(request.POST, prefix='resume_job')
        posted_education_forms = ResumeEducationFormset(request.POST, prefix='resume_education')
        posted_resume_jobs_section_title_form = ResumeJobsSectionTitleForm(request.POST)
        posted_resume_education_section_title_form = ResumeEducationSectionTitleForm(request.POST)
        # Cull out data for each form and formset
        if posted_resume_details.is_valid():
            form = posted_resume_details
            resume.resume_title=form.cleaned_data.get('resume_title')
            resume.contact_information_section_title=form.cleaned_data.get('contact_information_section_title')
            resume.contact_information=form.cleaned_data.get('contact_information')
            resume.personal_statement_section_title=form.cleaned_data.get('personal_statement_section_title')
            resume.personal_statement=form.cleaned_data.get('personal_statement')
            resume.current_skills_section_title=form.cleaned_data.get('current_skills_section_title')
            resume.current_skills=form.cleaned_data.get('current_skills')
            resume.save()
            forms['resume_details_form'] = ResumeDetailsForm(resume_detail_form_data)
        else:
            forms['resume_details_form'] = posted_resume_details

        if posted_resume_jobs.is_valid():  
            for form in posted_resume_jobs:
                if form.has_changed():
                    resume_job = form.save(commit=False)
                    resume_job.resume = resume
                    resume_job.save()
            forms['resume_jobs_formset'] = ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=request.user.resume.pk), prefix='resume_job')
        else:
            forms['resume_jobs_formset'] = posted_resume_jobs

        if posted_education_forms.is_valid():
            for form in posted_education_forms:
                if form.has_changed():
                    resume_education = form.save(commit=False)
                    resume_education.resume = resume
                    resume_education.save()
            forms['resume_education_formset'] = ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=request.user.resume.pk), prefix='resume_education')
        else:    
            forms['resume_education_formset'] = posted_education_forms
    else:
        profile_form_data = {'profile_active': request.user.resume.is_live }
        resume_jobs_section_title_form_data = {'resume_jobs_section_title': request.user.resume.resume_jobs_section_title}
        resume_education_section_title_form_data = {'resume_education_section_title': request.user.resume.resume_education_section_title}

        forms = {
            'activate_profile_form': ActivateResumeForm(profile_form_data),
            'resume_details_form': ResumeDetailsForm(resume_detail_form_data),
            'resume_jobs_section_title_form': ResumeJobsSectionTitleForm(resume_jobs_section_title_form_data),
            'resume_education_section_title_form': ResumeEducationSectionTitleForm(resume_education_section_title_form_data),
            'resume_jobs_formset': ResumeJobsFormset(queryset=ResumeJob.objects.filter(resume=request.user.resume.pk), prefix='resume_job'),
            'resume_education_formset': ResumeEducationFormset(queryset=ResumeEducation.objects.filter(resume=request.user.resume.pk), prefix='resume_education')
            }
    context = {
            'forms': forms,
            'resume_is_active': request.user.resume.is_live,
            'site_url': settings.SITE_URL,
            'constants': constants
            }
    return render(request, 'builder/builder.html', context)


@login_required
def toggle_resume_active(request):
    service = ResumeService()
    toggle_success = service.toggle_resume_active(request.user, request.POST)
    if toggle_success is not True:
        return HttpResponse(status=500)
    return HttpResponse(status=200)


@login_required
def preview_resume(request):
    service = ResumeService()
    content = service.preview_resume(request.POST)
    context = {'resume_content': content, 'is_preview': True, 'constants': constants}
    return render(request, 'builder/resume.html', context)


def view_resume(request, request_profile_url):
    service = ResumeService()
    resume = service.get_resume_by_profile_url(request_profile_url)
    if (resume is None):
        raise Http404(constants.PAGE_NOT_FOUND)
    resume_jobs = service.get_resume_jobs_by_id(resume.pk)
    resume_education = service.get_resume_education_by_id(resume.pk)
    if resume is not None:
        return render(request, 'builder/resume.html', {
            'resume': resume,
            'resume_jobs': resume_jobs,
            'resume_education': resume_education,
            'constants': constants
        })
    raise Http404(constants.PAGE_NOT_FOUND)
