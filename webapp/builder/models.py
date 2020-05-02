from django.contrib.auth.models import AbstractUser, User
from django.db import models
from accounts import constants


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_live = models.BooleanField(default=False, null=True)
    resume_title=models.CharField(max_length=500, null=True)
    personal_statement=models.TextField(null=True)
    current_skills=models.TextField(null=True)

class ResumeJob(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    position_title=models.CharField(max_length=500, null=True, blank=True)
    company_name=models.CharField(max_length=500, null=True, blank=True)
    start_date=models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    position_description=models.TextField(null=True, blank=True)

class ResumeEducation(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    education_title=models.CharField(max_length=500, null=True)
    institution_name=models.CharField(max_length=500, null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    degree_year=models.DateField(null=True)
    education_description=models.TextField(null=True)

