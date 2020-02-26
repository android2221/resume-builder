from django.urls import path

from .views import register_user, CustomLoginView
from .forms import UserLoginForm

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/',
        CustomLoginView.as_view(
            authentication_form=UserLoginForm,
        ),
    name='login')
]
