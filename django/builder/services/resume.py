from builder.forms import ResumeEditorForm, ActivateResumeForm
from django.conf import settings
import requests


class ResumeService():

    def get_resume_form(self, resume):
        editor_form_data = {'content': resume.content}
        profile_form_data = {'profile_active': resume.is_live }
        return {'editor_form': ResumeEditorForm(editor_form_data),
            'site_url': settings.SITE_URL,
            'activate_profile_form': ActivateResumeForm(profile_form_data) 
        }
    
    def save_resume_form(self, resume, payload):
        posted_form = ResumeEditorForm(payload)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            resume.content = form_data["content"]
            resume.save()
            requests.post(settings.MARKDOWN_RENDER_URL, data = {'markdownContent':resume.content})
            return True
        else:
            return False