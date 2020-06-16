from accounts import constants
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.conf import settings
from .services.resume_service import ResumeService
from django.contrib import messages

def handler404(request, exception):
    response = render(request, "builder/404.html", {})
    response.status_code = 404
    return response


def index(request):
    return render(request, 'builder/index.html', {})


@login_required
def builder_page(request):
    # Loading and saving resume page
    service = ResumeService()
    if request.POST:
        forms = service.save_resume(resume=request.user.resume, post_payload=request.POST)
        has_errors = False
        for form in forms.values():
            if form.errors:
                has_errors = True
                break
        if not has_errors:
            messages.success(request, constants.RESUME_SAVE_SUCCESS)
        else:
            messages.error(request, constants.ERROR_SAVING_RESUME)
    else:
        forms = service.init_forms(resume=request.user.resume)
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
    # saving and loading previews
    service = ResumeService()
    if request.POST:   
        forms = service.save_resume(resume=request.user.resume, post_payload=request.POST, is_preview=True)
    else:
        preview_resume = service.get_preview_resume(request.user.id)
        if (preview_resume is None):
            raise Http404(constants.PAGE_NOT_FOUND)
        preview_resume_jobs = service.get_resume_jobs_by_id(preview_resume.id)
        preview_resume_education = service.get_resume_education_by_id(preview_resume.id)
        if preview_resume is not None:
            return render(request, 'builder/resume.html', {
                'resume': preview_resume,
                'resume_jobs': preview_resume_jobs,
                'resume_education': preview_resume_education,
                'constants': constants
            })
    raise Http404(constants.PAGE_NOT_FOUND)


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
