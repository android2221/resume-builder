from django.urls import path
from django.views.generic import FormView

from . import views
from .forms import ResumeEditorForm
from builder.views import index as index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('builder/', views.builder, name='builder'),
    path('activate-resume/', views.toggle_resume_active, name='activate-resume'),
]