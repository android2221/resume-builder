from django.contrib.auth.models import AbstractUser, User
from django.db import models
from mdeditor.fields import MDTextField
from accounts import constants


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_live = models.BooleanField(default=False)
    content = MDTextField(default=constants.MARKDOWN_WELCOME)
    rendered_html_resume = models.TextField(default=constants.HTML_WELCOME)
