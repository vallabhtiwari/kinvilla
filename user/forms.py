from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
from .models import User, Resident


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]


class ResidentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    def __init__(self, *args, **kwargs):
        super(ResidentUpdateForm, self).__init__(*args, **kwargs)
        user = kwargs.get("instance").user
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name

    class Meta:
        model = Resident
        fields = [
            "first_name",
            "last_name",
            "father_name",
            "address",
            "profession",
            "work_address",
        ]

    def save(self, commit=True, *args, **kwargs):
        instance = super(ResidentUpdateForm, self).save(commit)
        user = instance.user
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.save()
        return instance
