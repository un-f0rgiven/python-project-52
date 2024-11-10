from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import translation


def dashboard_view(request):
    user_language = 'ru'
    translation.activate(user_language)
    request.LANGUAGE_CODE = user_language

    return render(request, 'task_manager/dashboard.html')


def index(request):
    return render(request, 'index.html', context={'name': 'Geralt'})


def user_list(request):
    users = User.objects.all()
    return render(request, 'task_manager/user_list.html', {'users': users})


def user_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Пользователь успешно создан.')
        return redirect('user_list')
    return render(request, 'task_manager/user_create.html')


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST['username']
        if request.POST.get('password'):
            user.set_password(request.POST['password'])
            user.save()
            messages.success(request, 'Пользователь успешно обновлен.')
            return redirect('user_list')
        return render(request, 'task_manager/user_update.html', {'user': user})


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удален.')
        return redirect('user_list')
    return render(request, 'task_manager/user_delete.html', {'user': user})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list')
        else:
            messages.error(request, 'Неверные данные пользователя или пароль.')
    return render(request, 'task_manager/user_login.html')


def user_logout(request):
    logout(request)
    return redirect('user_login')