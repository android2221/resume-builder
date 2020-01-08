from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class UserRegistrationForm(UserCreationForm):
    account_url = forms.CharField()

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
        try:
            user = User.objects.get(username=cleaned_data["email"])
        except ObjectDoesNotExist:
            user = None
        if user is not None:
            self.add_error("email", "That username already exists, please choose another")
