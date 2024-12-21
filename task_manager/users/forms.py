import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from task_manager.users.models import User

USERNAME_REGEX = r'^[\w.@+-]+$'

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.add_help_text()

    def add_help_text(self):
        self.fields['username'].help_text = (
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_.'
        )
        self.fields['password1'].help_text = (
            '<ul><li>Ваш пароль должен содержать '
            'как минимум 3 символа.</ul></li>'
        )
        self.fields['password2'].help_text = (
            'Для подтверждения введите, пожалуйста, пароль ещё раз.'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(USERNAME_REGEX, username):
            raise ValidationError(
                'Имя пользователя может содержать '
                'только буквы, цифры и символы @/./+/-/_.'
            )
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput, required=False
    )
    password2 = forms.CharField(
        label='Подтверждение пароля', widget=forms.PasswordInput, required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.add_help_text()

    def add_help_text(self):
        self.fields['password1'].help_text = (
            '<ul><li>Ваш пароль должен содержать '
            'как минимум 3 символа.</ul></li>'
        )
        self.fields['password2'].help_text = (
            'Для подтверждения введите, пожалуйста, пароль ещё раз.'
        )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")

        return cleaned_data


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Введите ваше имя пользователя.'