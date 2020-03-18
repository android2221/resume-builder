from builder import views
from django.urls import path, reverse_lazy
from django.views.generic import FormView

from .forms import ResumeEditorForm

urlpatterns = [
    path('', views.index, name='index'),
    path('builder/', views.load_builder, name='load_builder'),
    path('save-builder/', views.save_builder, name='save_builder'),
    path('builder/preview/', views.preview_resume, name='preview_resume'),
    path('activate-resume/', views.toggle_resume_active, name='activate_resume'),
]
