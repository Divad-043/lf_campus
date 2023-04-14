from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.gis import forms as lforms
from .models import Item, ItemCategory, ItemQuestion, Reclamation, DepositPoint, DepositPointAdministration, ItemDeposit
from accounts.models import User


# class UserForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name', 'questions']


class ItemQuestionForm(forms.ModelForm):
    class Meta:
        model = ItemQuestion
        fields = ['question', 'is_for_reclamation']


class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['user', 'item', 'question', 'response']


class DepositPointForm(forms.ModelForm):
    class Meta:
        model = DepositPoint
        fields = ['name', 'longitude', 'latitude', 'items', 'admins']


class DepositPointAdministrationForm(forms.ModelForm):
    class Meta:
        model = DepositPointAdministration
        fields = ['admin', 'deposit_point']


class ItemDepositForm(forms.ModelForm):
    class Meta:
        model = ItemDeposit
        fields = ['deposit_point', 'item', 'added_by']
