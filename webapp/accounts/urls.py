from django.urls import path

from .views import register_user, CustomLoginView, CustomForgotPasswordView, CustomSetPasswordView
from .forms import UserLoginForm, ResetForm, ResetConfirmForm

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
    path('<uidb64>/<token>/',
        CustomSetPasswordView.as_view(form_class=ResetConfirmForm),
        name="set_new_password" 
    )
]
