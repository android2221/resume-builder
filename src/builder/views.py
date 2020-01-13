# from django.shortcuts import render
# from django.http import HttpResponse

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from builder.forms import ResumeEditorForm, ActivateResumeForm
from .models import Resume
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

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
    print(request.POST)
    # form_data = {'profile_active': request.user.resume.is_live }
    # context = {"form": ActivateResumeForm(form_data) }
    # return HttpResponse(status=200)

def resume(request, profile_url):
    return render(request, 'builder/resume.html', {"profile_url": profile_url})
