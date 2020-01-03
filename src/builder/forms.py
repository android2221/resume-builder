from django import forms

from mdeditor.fields import MDTextFormField

class ResumeEditorForm (forms.Form):
    name = forms.CharField ()
    content = MDTextFormField ()
