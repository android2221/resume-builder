from accounts import constants
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from .services.resume import ResumeService

from .models import Resume

def index(request):
    context = {'some_sample_text': 'some sample i typed'}
    return render(request, 'builder/index.html', context)

@login_required
def builder(request):
    service = ResumeService()
    if request.POST:
        save_success = service.save_resume(request.user.resume, request.POST)
        return HttpResponseRedirect(reverse("builder"))
    else:
        context = service.get_resume_form(request.user.resume)
    return render(request, 'builder/builder.html', context)

@login_required
def toggle_resume_active(request):
    service = ResumeService()
    toggle_success = service.toggle_resume_active(request.user, request.POST)
    if toggle_success is not True:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

def view_resume(request, request_profile_url):
    service = ResumeService()
    rendered_resume = service.get_rendered_resume_content(request_profile_url)
    if rendered_resume is not None:
        return HttpResponse(rendered_resume)
    raise Http404(constants.PAGE_NOT_FOUND)