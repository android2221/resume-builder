from django import forms
from django.contrib.auth.models import User
from mdeditor.fields import MDTextFormField

class ResumeEditorForm (forms.Form):
    content = MDTextFormField ()
