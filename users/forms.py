from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        if password1 and len(password1) < 3:
            self.add_error(
                'password2',
                "Введённый пароль слишком короткий. "
                "Он должен содержать как минимум 3 символа."
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(
            pk=self.instance.pk
        ).filter(
            username=username
        ).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username
