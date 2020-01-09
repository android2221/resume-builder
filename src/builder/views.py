# from django.shortcuts import render
# from django.http import HttpResponse

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from builder.forms import ResumeEditorForm
from .models import ResumeTextModel
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
            resume = ResumeTextModel.objects.get(pk=form_data["resume_id"])
            resume.content = form_data["content"]
            resume.name = form_data["name"]
            resume.save()
            return HttpResponseRedirect(reverse('builder'))
    else:
        resume = request.user.resumetextmodel
        form_data = {'content': resume.content}
        context = {'form': ResumeEditorForm(form_data)}
    return render(request, 'builder/builder.html', context)
