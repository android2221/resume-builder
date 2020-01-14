from django.urls import path
from django.views.generic import FormView

from . import views
from .forms import ResumeEditorForm

urlpatterns = [
    path('edit/', views.builder, name='builder')
]