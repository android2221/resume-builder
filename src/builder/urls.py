from django.urls import path
from django.views.generic import FormView

from . import views
from .forms import ResumeEditorForm

urlpatterns = [
    path('', views.builder, name='builder')
]