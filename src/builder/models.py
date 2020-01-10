from django.db import models
from django.contrib.auth.models import AbstractUser, User
from mdeditor.fields import MDTextField

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    content = MDTextField()
