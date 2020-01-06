from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_user
    
urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name="password-reset")
]