from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .services.account_service import AccountService
from django.contrib.auth import views as auth_views
from . import constants


def register_user(request):
    service = AccountService()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('load_builder'))
    if request.POST:
        result = service.register_user(request)
        if result is True:
            # save worked, go to the builder
            return HttpResponseRedirect(reverse('load_builder'))
        else:
            context = {
                'form': service.build_registration_form(request.POST),
                'constants': constants
            }
            return render(request, 'registration/register.html', context)
    else:
        form = service.build_registration_form()
        context = {'form': form, "constants": constants}
        return render(request, 'registration/register.html', context)

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'constants': constants
        })
        return context