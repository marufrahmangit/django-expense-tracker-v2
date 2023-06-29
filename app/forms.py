from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Expense, Item


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")

        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['items'].queryset = self.fields['items'].queryset.filter(user=user)
        self.fields['items'].widget.attrs['class'] = 'item'
        self.fields['expense_method'].queryset = self.fields['expense_method'].queryset.filter(user=user)


class UploadForm(forms.Form):
    file = forms.FileField(label='Select a file')