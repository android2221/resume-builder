from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Account
from .forms import UserRegistrationForm
from django.urls import reverse

# Create your views here.
def register_user(request):
    # TODO: make sure normal password requirement failures are working (mismatched passwords, length off etc)
    if request.POST:
        posted_form = UserRegistrationForm(request.POST)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            user = User.objects.create_user(form_data["email"], form_data["email"], form_data["password1"])
            user.first_name = form_data["first_name"]
            user.last_name = form_data["last_name"]
            user.save()
            newaccount = Account(user=user, account_url=form_data["account_url"])
            newaccount.save()
            return HttpResponseRedirect(reverse('builder'))
        else:
            context = {'form': posted_form}
            return render(request, 'registration/register.html', context)
    context = {'form': UserRegistrationForm()}
    return render(request, 'registration/register.html', context)