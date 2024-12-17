from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from task_manager.users.models import User
from django.core.exceptions import ValidationError
import re


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
        self.fields['password1'].help_text = '<ul><li>Ваш пароль должен содержать как минимум 3 символа.</ul></li>'
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'

    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError('Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_.')
        
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем существует.')
        return username


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
        self.fields['password1'].help_text = '<ul><li>Ваш пароль должен содержать как минимум 3 символа.</ul></li>'
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'

    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError('Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_.')

        if User.objects.exclude(
            pk=self.instance.pk
        ).filter(
            username=username
        ).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']