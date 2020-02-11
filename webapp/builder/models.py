from django.contrib.auth.models import AbstractUser, User
from django.db import models
from accounts import constants


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_live = models.BooleanField(default=False)
    content = models.TextField()
    rendered_html_resume = models.TextField(default=constants.HTML_WELCOME)
