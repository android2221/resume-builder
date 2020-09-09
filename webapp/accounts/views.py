from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from honeypot.decorators import check_honeypot

from . import constants
from .services.account_service import AccountService


@check_honeypot(field_name='address1')
def register_user(request):
    service = AccountService()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('builder_page'))
    if request.POST:
        result = service.register_user(request)
        if result is True:
            # save worked, go to the builder
            return HttpResponseRedirect(reverse('builder_page'))
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
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'constants': constants
        })
        return context

class CustomForgotPasswordView(auth_views.PasswordResetView):
    template_name = "registration/password_reset_form.html"
    html_email_template_name = "registration/password_reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'constants': constants
        })
        return context

class CustomSetPasswordView(auth_views.PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'constants': constants
        })
        return context

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, constants.PASSWORD_CHANGE_SUCCESS)
        return super(auth_views.PasswordChangeView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(CustomPasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'constants': constants
        })
        return context
