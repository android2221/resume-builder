from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationViewTests(TestCase):
    def test_get_shouldreturn(self):
        response = self.client.get(reverse('register'), {})
        self.assertEqual(response.status_code, 200)

    def test_duplicate_username_should_return_error(self):
        user = User.objects.create_user("foo@bar.com", "foo@bar.com", "fakepassword")
        user.save()
        form_data = {
            "email": "foo@bar.com", 
            "password1": "fakepassword",
            "first_name": "test", 
            "last_name": "tester"
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertFormError(response, 'form', 'email', 'That username already exists, please choose another')
