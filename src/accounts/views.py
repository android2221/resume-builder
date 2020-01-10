from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Account
from builder.models import ResumeTextModel
from .forms import UserRegistrationForm
from django.urls import reverse

# Create your views here.
def register_user(request):
    # TODO: make sure normal password requirement failures are working (mismatched passwords, length off etc)
    if request.POST:
        posted_form = UserRegistrationForm(request.POST)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            user = create_user(form_data["email"], form_data["password1"], form_data["first_name"], form_data["last_name"])
            create_account(user, form_data["profile_url"])
            create_resume(user)
            login(request, user)
            return HttpResponseRedirect(reverse('builder'))
        else:
            context = {'form': posted_form}
            return render(request, 'registration/register.html', context)
    context = {'form': UserRegistrationForm()}
    return render(request, 'registration/register.html', context)

def create_user(email, password, first_name, last_name):
    user = User.objects.create_user(email, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user

def create_account(user, url):
    newaccount = Account(user=user, profile_url=url)
    newaccount.save()

def create_resume(user):
    newResume = ResumeTextModel(user=user, content="# Welcome!")
    newResume.save()
