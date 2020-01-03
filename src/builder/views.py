# from django.shortcuts import render
# from django.http import HttpResponse

from django.shortcuts import render, HttpResponse
from builder.forms import ResumeEditorForm
from .models import ResumeTextModel

def index(request):
    context = {'some_sample_text': 'some sample i typed'}
    return render(request, 'builder/index.html', context)

def builder(request):
    # We should only ever have one resume at a time per user
    resumes = ResumeTextModel.objects.all()
    if resumes.count() == 0:
        resume = ResumeTextModel()
        resume.save()
    else:
        resume = resumes[0]
        form_data = {'content': resume.content, 'name': resume.name}
    context = {'form': ResumeEditorForm(form_data), 'resumeid': resume.id}
    return render(request, 'builder/sampleform.html', context)

def save(request, resumeid):
    if request.POST:
        posted_form = ResumeEditorForm(request.POST)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            resume = ResumeTextModel.objects.get(pk=resumeid)
            resume.content = form_data["content"]
            resume.name = form_data["name"]
            resume.save()
        return HttpResponse("I HAVE BEEN POSTED: " + str(form_data["name"]))
