from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import register_user, CustomLoginView, CustomForgotPasswordView, CustomSetPasswordView
from .forms import UserLoginForm, ResetForm, ResetConfirmForm, CustomPasswordChangeForm

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/',
        CustomLoginView.as_view(
            authentication_form=UserLoginForm,
        ),
        name='login'
    ),
    path('password-reset/', 
        CustomForgotPasswordView.as_view(form_class=ResetForm), 
        name="reset_password"
    ),
    path('reset/<uidb64>/<token>/',
        CustomSetPasswordView.as_view(form_class=ResetConfirmForm),
        name="set_new_password" 
    ),
    path('password-change', 
        auth_views.PasswordChangeView.as_view(
            form_class=CustomPasswordChangeForm, 
            success_url=reverse_lazy('load_builder'),
        ), 
        name="change_password"
    )
]
