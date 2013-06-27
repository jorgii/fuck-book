from django import forms
from django.forms.extras.widgets import SelectDateWidget


class StatisticsForm(forms.Form):
    BASE_CHOICES = (('d', 'Daily'),
                    ('m', 'Monthly'))
    base = forms.ChoiceField(required=True, choices=BASE_CHOICES)
    from_t = forms.DateField(widget=SelectDateWidget, required=True)
    to_t = forms.DateField(widget=SelectDateWidget, required=True)
