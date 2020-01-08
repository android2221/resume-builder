from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    account_url = forms.CharField()

    class Meta:
        model = User
        fields = {"username", "first_name"}

    def clean(self):
        cleaned_data = self.cleaned_data
        existingUser = User.objects.get(username=cleaned_data["username"])
        if existingUser is not None:
            self.add_error("username", "That username already exists, please choose another!")


