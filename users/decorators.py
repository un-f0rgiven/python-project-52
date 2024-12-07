from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required as default_login_required,
)
from django.shortcuts import redirect


def login_required(view_func):
    decorated_view_func = default_login_required(view_func)

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Вы не авторизованы! Пожалуйста, выполните вход.'
            )
            return redirect('user_login')
        return decorated_view_func(request, *args, **kwargs)

    return wrapper
