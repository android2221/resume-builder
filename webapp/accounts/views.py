from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .services.account_service import AccountService


def register_user(request):
    service = AccountService()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('load_builder'))
    if request.POST:
        result = service.register_user(request)
        if result is True:
            # save worked go to the builder
            return HttpResponseRedirect(reverse('load_builder'))
        else:
            context = {'form': service.build_registration_form(request.POST)}
            return render(request, 'registration/register.html', context)
    else:
        form = service.build_registration_form()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

def login(request):
    service = AccountService()
    # return login form here :)

