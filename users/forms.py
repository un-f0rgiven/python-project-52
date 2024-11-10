from django import forms
from django.contrib.auth.models import User

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']