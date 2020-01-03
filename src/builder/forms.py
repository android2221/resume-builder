from django import forms

from mdeditor.fields import MDTextFormField

class ResumeEditorForm (forms.Form):
    name = forms.CharField ()
    resume_id = forms.CharField(widget=forms.HiddenInput())
    content = MDTextFormField ()
