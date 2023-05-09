from django import forms
from .models import Reclamation


class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['user', 'item', 'question', 'response']
