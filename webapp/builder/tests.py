from unittest.mock import MagicMock

import requests

from accounts.models import Account
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Resume


class FakeResponse(object):
    name = ""

class ResumeBuilderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("foo@bar.com", "foo@bar.com", "paas09df2@")
        self.resume_content = "initial content"
        resume = Resume(user=self.user)
        resume.content = self.resume_content
        resume.is_live = True
        resume.save()
        account = Account(user=self.user)
        account.profile_url = "fake-profile-url"
        account.save()
        self.authedClient = Client()
        self.authedClient.force_login(self.user)

    def test_login_required_redirect_works(self):
        response = self.client.get(reverse("builder_page"))
        self.assertRedirects(response, "/account/login/?next=/builder/")
    
    def test_can_builder_page_after_login(self):
        response = self.authedClient.get(reverse("builder_page"))
        self.assertEqual(response.status_code, 200)

    def test_save_resume_works(self):
        response_object = FakeResponse()
        response_object.text = "<h1>rendered thing</h1>"
        requests.post = MagicMock(return_value=response_object)
        form_data = {'resume_title': 'my test title', 
            'resume_job-TOTAL_FORMS': 1,
            'resume_job-INITIAL_FORMS': 0,
            'resume_job-MIN_NUM_FORMS': 0,
            'resume_job-MAX_NUM_FORMS': 1000,
            'resume_education-TOTAL_FORMS': 1,
            'resume_education-INITIAL_FORMS': 0,
            'resume_education-MIN_NUM_FORMS': 0,
            'resume_education-MAX_NUM_FORMS': 1000,
        } 
        response = self.authedClient.post(reverse("builder_page"), form_data)
        self.assertRedirects(response, reverse("builder_page"))

class ResumeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("foo@bar.com", "foo@bar.com", "paas09df2@")
        self.user.save()
        self.resume_content = "TITLEHERE"
        resume = Resume(user=self.user)
        resume.resume_title = self.resume_content
        resume.is_live = True
        resume.is_draft = False
        resume.save(force_insert=True)
        account = Account(user=self.user)
        account.profile_url = "fake-profile-url"
        account.save()
        self.authedClient = Client()
        self.authedClient.force_login(self.user)

    def test_active_resume_displays(self):
        resume = Resume(user=self.user)
        resume.resume_title = self.resume_content
        resume.is_live = True
        resume.is_draft = True
        resume.save(force_insert=True)
        response = self.client.get(reverse("view_resume", args=[self.user.account.profile_url]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.resume_content, str(response.content))
    
    def test_nonexistant_resume_returns_404(self):
        response = self.client.get(reverse("view_resume", args=["fakeurlthatdoesntexist"]))
        self.assertEqual(response.status_code, 404)
    
    def test_inactive_resume_returns_404(self):
        user = User.objects.create_user("foo1@bar.com", "foo1@bar.com", "paas09df2@")
        resume_content = "initial content2"
        resume = Resume(user=user)
        resume.content = resume_content
        resume.is_live = False
        resume.save()
        account = Account(user=user)
        account.profile_url = "fake-profile-url1"
        account.save()
        response = self.client.get(reverse("view_resume", args=[account.profile_url]))
        self.assertEqual(response.status_code, 404)
        
    def test_toggle_active_resume_success_returns_200(self):
        user = User.objects.create_user("fooasd@bar.com", "fooasd@bar.com", "paas09df2@")
        resume_content = "initial content"
        resume = Resume(user=user)
        resume.content = resume_content
        resume.is_live = False
        resume.save()
        account = Account(user=user)
        account.profile_url = "fake-profile-url2"
        account.save()
        authedClient = Client()
        authedClient.force_login(user)
        form_data = {
            "profile_active": True
        }
        response = authedClient.post(reverse("activate_resume"), form_data)
        self.assertEqual(response.status_code, 200)
        resumeResult = Resume.objects.get(user=user)
        self.assertEqual(resumeResult.is_live, True)
        form_data = {
            "profile_active": False
        }
        response = authedClient.post(reverse("activate_resume"), form_data)
        resumeResult = Resume.objects.get(user=user)
        self.assertEqual(resumeResult.is_live, False)

    def test_unauthenticated_resume_active_toggle_redirects(self):
        form_data = {
            "profile_active": "True"
        }
        response = self.client.post(reverse("activate_resume"), form_data)
        self.assertEqual(response.status_code, 302)
