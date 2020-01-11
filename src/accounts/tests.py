from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from . import constants
from .models import Account
from builder.models import Resume
from builder.views import builder as builderView
from .forms import UserRegistrationForm

class RegistrationViewTests(TestCase):
    form_data = {
            "email": "foo@bar.com", 
            "password1": "MRq%z393$SSUvSc",
            "password2": "MRq%z393$SSUvSc",
            "first_name": "test", 
            "last_name": "tester",
            "profile_url": "foo"
        }

    def test_load_registration_page_on_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_registration_post_should_create(self):
        self.client.post(reverse("register"), self.form_data)
        user = User.objects.get(username=self.form_data["email"])
        self.assertIsInstance(user.account, Account)
        self.assertIsInstance(user.resume, Resume)
        self.assertEqual(user.resume.content, constants.MARKDOWN_WELCOME)

    def test_registration_post_creates_account_information(self):
        self.client.post(reverse("register"), self.form_data)
        user = User.objects.get(username=self.form_data["email"])
        self.assertEqual(self.form_data["email"], user.email)
        self.assertEqual(self.form_data["first_name"], user.first_name)
        self.assertEqual(self.form_data["last_name"], user.last_name)
        self.assertEqual(self.form_data["profile_url"], user.account.profile_url)

    def test_registration_redirects_to_builder(self):
        response = self.client.post(reverse("register"), self.form_data)
        self.assertRedirects(response, reverse("builder"))

    # Test rendering of our form errors
    def test_duplicate_username_should_return_error(self):
        User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
        response = self.client.post(reverse("register"), self.form_data)
        self.assertFormError(response, "form", "email", constants.ERROR_DUPLICATE_EMAIL)

    def test_duplicate_profileurl_should_return_error(self):
        user = User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
        account = Account(user=user, profile_url="foo")
        account.save()
        response = self.client.post(reverse("register"), self.form_data)
        self.assertFormError(response, "form", "profile_url", constants.ERROR_DUPLICATE_PROFILE_URL)

class RegistrationFormTests(TestCase):
        form_data = {
            "email": "foo@bar.com", 
            "password1": "MRq%z393$SSUvSc",
            "password2": "MRq%z393$SSUvSc",
            "first_name": "test", 
            "last_name": "tester",
            "profile_url": "foo"
        }
        
        def test_no_duplicate_profile_is_valid(self):
            form = UserRegistrationForm(data=self.form_data)
            self.assertTrue(form.is_valid())

        # Test our custom cleaning stuff
        def test_duplicate_username_invalidates_form(self):
            User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
            form = UserRegistrationForm(data=self.form_data)
            self.assertIn(constants.ERROR_DUPLICATE_EMAIL, str(form.errors))

        def test_duplicate_profile_url_invalidates_form(self):
            user = User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
            account = Account(user=user)
            user.account.profile_url = "foo"
            account.save()
            form = UserRegistrationForm(data=self.form_data)
            self.assertFalse(form.is_valid())
            self.assertIn(constants.ERROR_DUPLICATE_PROFILE_URL, str(form.errors))
        
        def test_good_profile_url_form_valid(self):
            form_data = self.form_data.copy()
            form = UserRegistrationForm(data=form_data)
            self.assertTrue(form.is_valid())
            form_data["profile_url"] = "this-has-hyphens-and-should-work"
            form = UserRegistrationForm(data=form_data)
            self.assertTrue(form.is_valid())
            form_data["profile_url"] = "this_has_underscores_and_should_work"
            form = UserRegistrationForm(data=form_data)
            self.assertTrue(form.is_valid())

        def test_malformed_profile_url_invalidate_form(self):
            form_data = self.form_data.copy()
            form_data["profile_url"] = "*@@"
            form = UserRegistrationForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn(constants.FORM_PROFILE_URL_REQUIREMENTS, str(form.errors))
            form_data["profile_url"] = "thishasa space"
            form = UserRegistrationForm(data=form_data)
            self.assertFalse(form.is_valid())
            form_data["profile_url"] = "thishasa space"
            form = UserRegistrationForm(data=form_data)
            self.assertFalse(form.is_valid())

class ResumeBuilderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("foo@bar.com", "foo@bar.com", "paas09df2@")
        self.resume_content = "initial content"
        resume = Resume(user=self.user)
        resume.content = self.resume_content
        resume.save()
        account = Account(user=self.user)
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
        form_data = {
            "content": "# My test thing"
        }
        response = self.authedClient.post(reverse("builder"), form_data)
        self.assertRedirects(response, reverse("builder"))


## Password flow tests
# login/ logout redirects etc

 ## BUILDER TESTS
  # publishing -> don't display if 'publish' isn't turned on and the converse

 # can't access someone elses resume edit page should load my resume only

 # resume pages that aren't public don't load
