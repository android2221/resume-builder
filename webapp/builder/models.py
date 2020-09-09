from accounts import constants
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=True)
    is_live = models.BooleanField(default=False, null=True, blank=True)
    resume_title=models.CharField(max_length=500, null=True, blank=True)
    contact_information=models.TextField(null=True, blank=True)
    personal_statement=models.TextField(null=True, blank=True)
    current_skills=models.TextField(null=True, blank=True)
    contact_information_section_title=models.CharField(max_length=500, null=True, blank=True, default='Contact Information')
    personal_statement_section_title=models.CharField(max_length=500, null=True, blank=True, default='Personal Statement')
    current_skills_section_title=models.CharField(max_length=500, null=True, blank=True, default='Current Skills')
    resume_jobs_section_title=models.CharField(max_length=500, null=True, blank=True, default='Experience')
    resume_education_section_title=models.CharField(max_length=500, null=True, blank=True, default='Education')

class ResumeJob(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    position_title=models.CharField(max_length=500)
    company_name=models.CharField(max_length=500)
    start_date=models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    position_description=models.TextField(null=True, blank=True)
    is_current=models.BooleanField(default=False)
    resume_position=models.IntegerField(null=True, blank=True)

class ResumeEducation(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    education_title=models.CharField(max_length=500)
    institution_name=models.CharField(max_length=500)
    completed_date=models.DateField(null=True, blank=True)
    education_description=models.TextField(null=True, blank=True)
    is_current=models.BooleanField(default=False)
    resume_position=models.IntegerField(null=True, blank=True)
