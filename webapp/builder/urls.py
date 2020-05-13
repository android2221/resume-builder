from builder import views
from django.urls import path, reverse_lazy
from django.views.generic import FormView

urlpatterns = [
    path('', views.index, name='index'),
    path('builder/', views.builder_page, name='builder_page'),
    path('builder/preview/', views.preview_resume, name='preview_resume'),
    path('activate-resume/', views.toggle_resume_active, name='activate_resume'),
]
