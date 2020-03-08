from django.urls import path

from .views import register_user, CustomLoginView, CustomForgotPasswordView
from .forms import UserLoginForm, ResetForm

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
    )
]
