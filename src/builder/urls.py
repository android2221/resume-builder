from django.urls import path
from django.views.generic import FormView

from . import views
from .forms import MDEditorForm

urlpatterns = [
    path('', views.index, name='index'),
    path('builder', views.builder, name='builder'),
    path('sampleform', FormView.as_view(template_name="builder/sampleform.html",
                                form_class=MDEditorForm))
]