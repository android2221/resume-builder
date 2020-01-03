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
    context = {'form': ResumeEditorForm, 'resumeid': resume.id}
    return render(request, 'builder/sampleform.html', context)

def save(request, resumeid):
    if request.POST:
        return HttpResponse("I HAVE BEEN POSTED: " + str(resumeid))
