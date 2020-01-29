from accounts.forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from accounts.models import Account
from builder.models import Resume
from accounts import constants

class AccountService():
    
    def register_user(self, request):
        posted_form = UserRegistrationForm(request.POST)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            user = self.create_account(form_data)
            login(request, user)
            return True
        else:
            return False

    def create_account(self, form_data):
        user = User.objects.create_user(form_data["email"], form_data["email"], form_data["password1"])
        user.first_name = form_data["first_name"]
        user.last_name = form_data["last_name"]
        user.save()
        newaccount = Account(user=user, profile_url=form_data["profile_url"])
        newaccount.save()
        self.create_resume(user)
        return user

    def build_registration_form(self, payload=None):
        if payload is None:
            return payload
        return UserRegistrationForm(payload)

    def create_user(email, password, first_name, last_name):
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def create_resume(self, user):
        newResume = Resume(user=user, content=constants.MARKDOWN_WELCOME)
        newResume.save()