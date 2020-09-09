from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .forms import (CustomPasswordChangeForm, ResetConfirmForm, ResetForm,
                    UserLoginForm)
from .views import (CustomForgotPasswordView, CustomLoginView,
                    CustomPasswordChangeView, CustomSetPasswordView,
                    register_user)

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
        CustomPasswordChangeView.as_view(
            form_class=CustomPasswordChangeForm, 
            success_url=reverse_lazy('builder_page'),
        ), 
        name="change_password"
    )
]
