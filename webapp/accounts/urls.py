from django.contrib.auth import views as auth_views
from django.urls import path

from .views import register_user
from .forms import UserLoginForm

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/',
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
        ),
    name='login')
]
