import re

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from . import constants, patterns
from .models import Account


class UserRegistrationForm(auth_forms.UserCreationForm):
    profile_url = forms.CharField(help_text=constants.FORM_PROFILE_URL_REQUIREMENTS)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['first_name'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['last_name'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['password1'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['password2'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['profile_url'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['email'].widget.attrs['placeholder'] = constants.FORM_EMAIL_PLACEHOLDER
        self.fields['first_name'].widget.attrs['placeholder'] = constants.FORM_FIRST_NAME_PLACEHOLDER
        self.fields['last_name'].widget.attrs['placeholder'] = constants.FORM_LAST_NAME_PLACEHOLDER
        self.fields['password1'].widget.attrs['placeholder'] = constants.FORM_PASSWORD_PLACEHOLDER
        self.fields['password2'].widget.attrs['placeholder'] = constants.FORM_PASSWORD_CONFIRM_PLACEHOLDER
        self.fields['profile_url'].widget.attrs['placeholder'] = constants.FORM_PROFILE_URL_PLACEHOLDER

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean(self):
        cleaned_data = self.cleaned_data
        is_username_duplicate = check_duplicate_username(cleaned_data["email"])
        profile_url_result = check_profile_url(cleaned_data["profile_url"])
        is_profile_url_duplicate = check_duplicate_profile_url(cleaned_data["profile_url"])
        try:
            self.cleaned_data["profile_url"] = self.cleaned_data["profile_url"].lower()
        except:
            self.add_error("profile_active", constants.ERROR_PARSING_PROFILE_URL)
        if is_username_duplicate:
            self.add_error("email", constants.ERROR_DUPLICATE_EMAIL)
        if profile_url_result == False:
            self.add_error("profile_url", constants.FORM_PROFILE_URL_REQUIREMENTS)
        if is_profile_url_duplicate:
            self.add_error("profile_url", constants.ERROR_DUPLICATE_PROFILE_URL)

    field_order = ['profile_url', 'email', 'first_name', 'last_name', 'password1', 'password2']

def check_duplicate_username(email):
    try:
        user = User.objects.get(username=email)
        if (user is not None):
            return True
    except ObjectDoesNotExist:
        return False

def check_duplicate_profile_url(url):
    try:
        account = Account.objects.get(profile_url=url)
        if (account is not None):
            return True
    except ObjectDoesNotExist:
        return False

def check_profile_url(profile_url):
    pattern = re.compile(patterns.PROFILE_URL_PATTERN)
    match = pattern.match(profile_url)
    if match is None:
        return False
    return True

class UserLoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['password'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['username'].widget.attrs['placeholder'] = constants.FORM_USERNAME_PLACEHOLDER
        self.fields['password'].widget.attrs['placeholder'] = constants.FORM_PASSWORD_PLACEHOLDER

class ResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = constants.FORM_EMAIL_PLACEHOLDER
        self.fields['email'].widget.attrs['class'] = constants.INPUT_STYLE_NAME

class ResetConfirmForm(auth_forms.SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super(ResetConfirmForm, self).__init__(user, *args, **kwargs)
        self.user = user
        self.fields['new_password1'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['new_password2'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['new_password1'].widget.attrs['placeholder'] = constants.FORM_NEW_PASSWORD_PLACEHOLDER
        self.fields['new_password2'].widget.attrs['placeholder'] = constants.FORM_PASSWORD_CONFIRM_PLACEHOLDER

class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(user, *args, **kwargs)
        self.user = user
        self.fields['old_password'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['new_password1'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['new_password2'].widget.attrs['class'] = constants.INPUT_STYLE_NAME
        self.fields['new_password1'].widget.attrs['placeholder'] = constants.FORM_NEW_PASSWORD_PLACEHOLDER
        self.fields['new_password2'].widget.attrs['placeholder'] = constants.FORM_CONFIRM_NEW_PASSWORD
        self.fields['old_password'].widget.attrs['placeholder'] = constants.FORM_OLD_PASSWORD_PLACEHOLDER
