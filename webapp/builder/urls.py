from builder import views
from django.urls import path, reverse_lazy
from django.views.generic import FormView, TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('terms/', TemplateView.as_view(template_name="builder/terms.html"), name="terms"),
    path('privacy/', TemplateView.as_view(template_name="builder/privacy.html"), name="privacy"),
    path('builder/', views.builder_page, name='builder_page'),
    path('builder/preview/', views.preview_resume, name='preview_resume'),
    path('builder/publish/', views.publish_resume, name='publish_resume'),
    path('activate-resume/', views.toggle_resume_active, name='activate_resume'),
]
