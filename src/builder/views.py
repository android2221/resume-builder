# from django.shortcuts import render
# from django.http import HttpResponse

from django.shortcuts import render, HttpResponse
from builder.forms import ResumeEditorForm
from .models import ResumeTextModel

def index(request):
    context = {'some_sample_text': 'some sample i typed'}
    return render(request, 'builder/index.html', context)

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
    else:
        # We should only ever have one resume at a time per user
        resumes = ResumeTextModel.objects.all()
        if resumes.count() == 0:
            # Create a new form, this user doesn't have a resume
            resume = ResumeTextModel()
            resume.save()
        else:
            # This user has a form, bind the data
            resume = resumes[0]
    form_data = {'content': resume.content, 'name': resume.name, 'resume_id': resume.id}
    context = {'form': ResumeEditorForm(form_data)}
    return render(request, 'builder/builder.html', context)
