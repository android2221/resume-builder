from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from . import constants
from .models import Account

class RegistrationViewTests(TestCase):
    def test_get_shouldreturn(self):
        response = self.client.get(reverse("register"), {})
        self.assertEqual(response.status_code, 200)

    def test_duplicate_username_should_return_error(self):
        User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
        form_data = {
            "email": "foo@bar.com", 
            "password1": "fakepassword",
            "first_name": "test", 
            "last_name": "tester",
            "profile_url": "foo"
        }
        response = self.client.post(reverse("register"), form_data)
        self.assertFormError(response, "form", "email", constants.ERROR_DUPLICATE_EMAIL)

    def test_duplicate_profileurl_should_return_error(self):
        user = User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
        account = Account(user=user, profile_url="foo")
        account.save()
        form_data = {
            "email": "foo@bar.com", 
            "password1": "fakepassword",
            "first_name": "test", 
            "last_name": "tester",
            "profile_url": "foo"
        }
        response = self.client.post(reverse("register"), form_data)
        self.assertFormError(response, "form", "profile_url", constants.ERROR_DUPLICATE_PROFILE_URL)



# profile url can only be url compliant
 # register user should create account
 # "" should create resume