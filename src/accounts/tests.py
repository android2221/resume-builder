from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from . import constants
from .models import Account
from builder.models import Resume
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
        
        # Test our custom cleaning stuff
        def test_registration_form_is_valid(self):
            User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
            form = UserRegistrationForm(data=self.form_data)
            self.assertIn(constants.ERROR_DUPLICATE_EMAIL, str(form.errors))

## Form tests
# invalid form should return to form partially filled out w/ errors (this is already sorta covered)
 # profile url can only be url compliant, block on backend and frontend REGEX: ^[a-zA-Z\d-_]+$  


 ## BUILDER TESTS
 # should load my resume only
 # not logged in should return to login
 # saving works