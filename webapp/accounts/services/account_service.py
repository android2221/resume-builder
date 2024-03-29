from accounts import constants
from accounts.forms import UserRegistrationForm, UserLoginForm
from accounts.models import Account
from builder.models import Resume
from django.contrib.auth import login
from django.contrib.auth.models import User


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
        self.create_preview_resume(user)
        return user

    def build_registration_form(self, payload=None):
        if payload is None:
            return UserRegistrationForm()
        return UserRegistrationForm(payload)
    
    def build_login_form(self, payload=None):
        if payload is None:
            return UserLoginForm()
        return UserLoginForm(payload)

    def create_user(self, email, password, first_name, last_name):
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def create_resume(self, user):
        newResume = Resume(user=user, is_draft=False)
        newResume.save()
    
    def create_preview_resume(self, user):
        preview_resume = Resume(user=user, is_draft=True)
        preview_resume.save()
