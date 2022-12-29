from django import forms
from django.forms import ModelForm, TextInput, PasswordInput


class LoginForm(forms.Form):
    widgets = {
        "username": TextInput(attrs={
            'class': 'form-control rounded-3 form-control-lg  my-2',
            'placeholder': 'Логин'
        }),
        "password": PasswordInput(attrs={
            'class': 'form-control rounded-3 form-control-lg my-2',
            'placeholder': 'Пароль'
        })
    }
    username = forms.CharField(max_length=50, widget=widgets['username'])
    password = forms.CharField(max_length=50, widget=widgets['password'])
