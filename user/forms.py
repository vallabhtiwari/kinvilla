from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]
