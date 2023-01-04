from django import forms
from . import models


class PeriodForm(forms.ModelForm):
    class Meta:
        model = models.Period
        fields = ['cutoff', 'payday']
        widgets = {
            'cutoff': forms.DateInput(attrs={'type': 'date'}),
            'payday': forms.DateInput(attrs={'type': 'date'})
        }


class ShiftForm(forms.ModelForm):
    class Meta:
        model = models.Shift
        fields = ["start", "finish"]
        widgets = {
            'start': forms.DateInput(attrs={'type': 'datetime-local'}),
            'finish': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class ShiftFormAlt(forms.ModelForm):
    class Meta:
        model = models.Shift
        fields = ["start", "length"]
        widgets = {
            'start': forms.DateInput(attrs={'type': 'datetime-local'}),
        }
