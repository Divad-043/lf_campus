from django import forms
from .models import ItemIdentifier, ItemIdentifierType


class ItemIdentifierForm(forms.ModelForm):
    class Meta:
        model = ItemIdentifier
        fields = ['item_name', 'identifier_type', 'expire_date']
        widgets = {
            'expire_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
