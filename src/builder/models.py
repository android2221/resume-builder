from django.db import models
from django.contrib.auth.models import AbstractUser
from mdeditor.fields import MDTextField

class ResumeTextModel(models.Model):
    name = models.CharField(max_length=10)
    content = MDTextField()

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username