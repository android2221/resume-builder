from builder.views import BuilderViews
from django.urls import path
from django.views.generic import FormView

from .views import BuilderViews
from .forms import ResumeEditorForm

urlpatterns = [
    path('', BuilderViews.index, name='index'),
    path('builder/', BuilderViews.builder , name='builder'),
    path('activate-resume/', BuilderViews.toggle_resume_active, name='activate-resume'),
]
