from django.db import models
from django.contrib.auth.models import AbstractUser
from mdeditor.fields import MDTextField

class ResumeTextModel(models.Model):
    name = models.CharField(max_length=10)
    content = MDTextField()
