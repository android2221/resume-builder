from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .services.account import AccountService


def register_user(request):
    service = AccountService()
    if request.POST:
        result = service.register_user(request)
        if result is True:
            # save worked go to the builder
            return HttpResponseRedirect(reverse('builder'))
        else:
            context = {'form': service.build_registration_form(request.POST)}
            return render(request, 'registration/register.html', context)
    else:
        form = service.build_registration_form()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

