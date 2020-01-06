from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_user
    
urlpatterns = [
    path('register/', register_user),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view()),
    path('password-reset/', auth_views.PasswordResetView.as_view())
]