from accounts import constants
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.conf import settings
from .services.resume_service import ResumeService
from django.contrib import messages


def index(request):
    context = {'some_sample_text': 'some sample thing i typed'}
    return render(request, 'builder/index.html', context)

@login_required
def save_builder(request):
    service = ResumeService()
    if request.POST:
        save_success = service.save_resume(request.user.resume, request.POST)
        if save_success == False:
            messages.error(request, constants.ERROR_SAVING_RESUME )
        return HttpResponseRedirect(reverse("load_builder"))

@login_required
def load_builder(request):
    service = ResumeService()
    forms = service.build_resume_forms(request.user.resume)
    context = { 'forms': forms, 
        'resume_is_active': request.user.resume.is_live,
        'site_url': settings.SITE_URL,
        'resume_active_message': constants.RESUME_IS_PUBLISHED,
        'resume_not_active_message': constants.RESUME_NOT_PUBLISHED,
        'activate_resume_header': constants.ACTIVATE_RESUME_HEADER,
        'not_live_text': constants.NOT_LIVE_TEXT,
        'live_text': constants.LIVE_TEXT,
        'save_button': constants.RESUME_SAVE_BUTTON,
        'preview_button': constants.RESUME_PREVIEW_BUTTON
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
    context = {'resume_content': content}
    return render(request, 'builder/preview-resume.html', context)

def view_resume(request, request_profile_url):
    service = ResumeService()
    rendered_resume = service.get_rendered_resume_content(request_profile_url)
    if rendered_resume is not None:
        return render(request, 'builder/resume.html', {"resume_content": rendered_resume})
    raise Http404(constants.PAGE_NOT_FOUND)
