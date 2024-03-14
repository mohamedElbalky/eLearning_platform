"""
Django comes with an abstraction layer to work with multiple forms on the same page. These groups
of forms are known as formsets. Formsets manage multiple instances of a certain Form or ModelForm.
All forms are submitted at once and the formset takes care of the initial number of forms to display,
limiting the maximum number of forms that can be submitted and validating all the forms.
"""

from django import forms

from django.forms.models import inlineformset_factory


from .models import Course, Module


ModuleFormSet = inlineformset_factory(
    Course, Module, fields=["title", "description"], extra=2, can_delete=True
)
