from django.shortcuts import render, HttpResponse
from .forms import UserRegistrationForm

# Create your views here.
def register_user(request):
    # TODO: make sure normal password requirement failures are working (mismatched passwords, length off etc)
    if request.POST:
        posted_form = UserRegistrationForm(request.POST)
        if posted_form.is_valid():
            form_data = posted_form.cleaned_data
            return HttpResponse(form_data["account_url"])
    context = {'form': UserRegistrationForm()}
    return render(request, 'registration/register.html', context)