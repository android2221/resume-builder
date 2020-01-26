import requests
from accounts import constants
from accounts.models import Account
from builder.forms import ActivateResumeForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
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
    manager = ResumeService()
    # Save logic
    if request.POST:
        save_success = manager.save_resume_form(request.user.resume, request.POST)
        return HttpResponseRedirect(reverse("builder"))
    else:
        context = manager.get_resume_form(request.user.resume)
    return render(request, 'builder/builder.html', context)

@login_required
def toggle_resume_active(request):
    if request.user.is_anonymous:
        return HttpResponse(status=401)
    form = ActivateResumeForm(request.POST)
    if form.is_valid():
        try:
            request.user.resume.is_live = form.cleaned_data["profile_active"]
            request.user.resume.save()
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

def resume(request, request_profile_url):
    if request_profile_url is None:
        raise Http404(constants.PAGE_NOT_FOUND)
    try:
        account = Account.objects.get(profile_url=request_profile_url)
    except ObjectDoesNotExist:
        account = None
    if account is None or account.user.resume.is_live == False:
        raise Http404(constants.PAGE_NOT_FOUND)
    return HttpResponse(account.user.resume.content)
