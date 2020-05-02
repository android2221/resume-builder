from django.contrib.auth.models import AbstractUser, User
from django.db import models
from accounts import constants


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_live = models.BooleanField(default=False, null=True)
    resume_title=models.CharField(max_length=500, null=True)
    personal_statement=models.TextField(null=True)
    current_skills=models.TextField(null=True)
    rendered_html_resume = models.TextField(default=constants.HTML_WELCOME)

class ResumeJob(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    position_title=models.CharField(max_length=500, null=True)
    company_name=models.CharField(max_length=500, null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    position_description=models.TextField(null=True)

class ResumeEducation(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    education_title=models.CharField(max_length=500, null=True)
    institution_name=models.CharField(max_length=500, null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    degree_year=models.DateField(null=True)
    education_description=models.TextField(null=True)

