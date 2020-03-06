from django.urls import path

from .views import register_user, CustomLoginView, CustomForgotPasswordView
from .forms import UserLoginForm

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/',
        CustomLoginView.as_view(
            authentication_form=UserLoginForm,
        ),
    name='login'),
    path('password-reset/', CustomForgotPasswordView.as_view(), name="reset_password")
]
