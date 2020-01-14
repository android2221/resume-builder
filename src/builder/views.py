# from django.shortcuts import render
# from django.http import HttpResponse

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from builder.forms import ResumeEditorForm, ActivateResumeForm
from .models import Resume
from accounts.models import Account
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404
from accounts import constants

def index(request):
    context = {'some_sample_text': 'some sample i typed'}
    return render(request, 'builder/index.html', context)

@login_required
def builder(request):
    # Save logic
    if request.POST:
        posted_form = ResumeEditorForm(request.POST)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            resume = request.user.resume
            resume.content = form_data["content"]
            resume.save()
            return HttpResponseRedirect(reverse("builder"))
    else:
        resume = request.user.resume
        editor_form_data = {'content': resume.content}
        profile_form_data = {'profile_active': request.user.resume.is_live }
        context = {'editor_form': ResumeEditorForm(editor_form_data),
            'site_url': settings.SITE_URL,
            'activate_profile_form': ActivateResumeForm(profile_form_data) 
        }
    return render(request, 'builder/builder.html', context)

@login_required
def toggle_resume_active(request):
    form = ActivateResumeForm(request.POST)
    if form.is_valid():
        request.user.resume.is_live = form.cleaned_data["profile_active"]
        request.user.resume.save()
        return HttpResponse(status=200)
    # return a failure if it doesn't work

    # TODO: Fix resume URL getting ran everytime
    # TODO: flesh out JS erroring
    # TODO: write tests for resume active toggle
    # TODO: return failure from resume activate if it doesn't work

def resume(request, request_profile_url):
    if request_profile_url is None:
        return Http404(constants.PAGE_NOT_FOUND)
    account = Account.objects.get(profile_url=request_profile_url)
    if account is None or account.user.resume.is_live == False:
        return HttpResponse(constants.PAGE_NOT_FOUND)
    return HttpResponse(account.user.resume.content)


