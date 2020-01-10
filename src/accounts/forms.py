from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account
from django.core.exceptions import ObjectDoesNotExist
from . import constants

class UserRegistrationForm(UserCreationForm):
    profile_url = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Making fields required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = {"email", "first_name", "last_name"}

    def clean(self):
        cleaned_data = self.cleaned_data
        is_username_duplicate = check_duplicate_username(cleaned_data["email"])
        is_profile_url_duplicate = check_duplicate_profile_url(cleaned_data["profile_url"])
        if is_username_duplicate:
            self.add_error("email", constants.ERROR_DUPLICATE_EMAIL)
        if is_profile_url_duplicate:
            self.add_error("profile_url", constants.ERROR_DUPLICATE_PROFILE_URL)

def check_duplicate_username(email):
    try:
        user = User.objects.get(username=email)
        if (user is not None):
            print("found user")
            return True
    except ObjectDoesNotExist:
        return False

def check_duplicate_profile_url(url):
    try:
        print("getting account")
        account = Account.objects.get(profile_url=url)
        if (account is not None):
            return True
    except ObjectDoesNotExist:
        print("no account found")
        return False

