from django.urls import path
from django.views.generic import FormView

from . import views
from .forms import ResumeEditorForm

urlpatterns = [
    path('', views.index, name='index'),
    path('builder', views.builder, name='builder'),
    path('resume/<int:resumeid>/save/', views.save, name='save'),
]