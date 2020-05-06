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
def save_builder(request):
    service = ResumeService()
    if request.POST:
        save_success = service.save_resume(request.user.resume, request.POST)
        if not save_success:
            messages.error(request, constants.ERROR_SAVING_RESUME)
        else:
            messages.success(request, constants.RESUME_SAVE_SUCCESS)
        return HttpResponseRedirect(reverse("load_builder"))


@login_required
def load_builder(request):
    service = ResumeService()
    forms = service.build_resume_forms(request)
    context = {'forms': forms,
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
