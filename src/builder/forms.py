from django import forms

from mdeditor.fields import MDTextFormField

class MDEditorForm (forms.Form):
    name = forms.CharField ()
    content = MDTextFormField ()
