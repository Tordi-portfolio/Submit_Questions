from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.Form):

    full_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    phone_number = forms.CharField(max_length=20)
    telegram_username = forms.CharField(required=False)
    country = forms.CharField(max_length=100)
    age = forms.IntegerField()

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)