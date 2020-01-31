from builder.forms import ResumeEditorForm, ActivateResumeForm
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from accounts.models import Account
import requests


class ResumeService():

    def get_rendered_resume_content(self, request_profile_url):
        try:
            account = Account.objects.get(profile_url=request_profile_url)
        except ObjectDoesNotExist:
            return None
        if account.user.resume.is_live is True:
            return account.user.resume.rendered_html_resume
        return None
    
    def build_resume_form(self, resume):
        editor_form_data = {'content': resume.content}
        profile_form_data = {'profile_active': resume.is_live }
        return {'editor_form': ResumeEditorForm(editor_form_data),
            'site_url': settings.SITE_URL,
            'activate_profile_form': ActivateResumeForm(profile_form_data) 
        }
    
    def save_resume(self, resume, payload):
        posted_form = ResumeEditorForm(payload)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            resume.content = form_data["content"]
            rendered_resume = requests.post(settings.MARKDOWN_RENDER_URL, 
                data = {'markdownContent': resume.content}
            )
            resume.rendered_html_resume = rendered_resume.text
            resume.save()
            return True
        else:
            print("poste form is not valid")
            return False
    
    def toggle_resume_active(self, user, payload):
        form = ActivateResumeForm(payload)
        if form.is_valid():
            try:
                user.resume.is_live = form.cleaned_data["profile_active"]
                user.resume.save()
                return True
            except:
                return False
