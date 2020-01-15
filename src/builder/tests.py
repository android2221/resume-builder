from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Resume
from accounts.models import Account

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
        response = self.client.get(reverse("builder"))
        self.assertRedirects(response, "/account/login/?next=/builder/")
    
    def test_can_load_builder_after_login(self):
        response = self.authedClient.get(reverse("builder"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.resume_content, str(response.content))

    def test_save_resume_works(self):
        form_data = {"content": "# My test thing"}
        response = self.authedClient.post(reverse("builder"), form_data)
        self.assertRedirects(response, reverse("builder"))


class ResumeViewTests(TestCase):
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

    def test_active_resume_displays(self):
        response = self.client.get(reverse("resume", args=[self.user.account.profile_url]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.resume_content, str(response.content))
    
    def test_nonexistant_resume_returns_404(self):
        response = self.client.get(reverse("resume", args=["fakeurlthatdoesntexist"]))
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
        response = self.client.get(reverse("resume", args=[account.profile_url]))
        self.assertEqual(response.status_code, 404)

 # can't access someone elses resume edit page should load my resume only
# POST to profile toggle toggles profile