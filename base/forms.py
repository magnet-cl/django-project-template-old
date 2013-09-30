from django import forms
from django.db import models


def make_custom_datefield(f):
    formfield = f.formfield()

    if isinstance(f, models.DateField):
        formfield.widget.format = '%d/%m/%Y'
        formfield.widget.attrs.update({'class': 'date-picker'})
    return formfield


class BaseForm(forms.ModelForm):
    formfield_callback = make_custom_datefield

    pass
