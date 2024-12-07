from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.forms import UserCreateForm, UserUpdateForm
from users.decorators import login_required


def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован.')
            return redirect('user_login')
        else:
            pass
    else:
        form = UserCreateForm()

    return render(request, 'users/user_create.html', {'form': form})


@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        messages.error(
            request,
            "У вас нет прав для изменения другого пользователя."
        )
        return redirect('user_list')

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        password1 = request.POST.get('password1')
        print(f'password1: {password1}')
        password2 = request.POST.get('password2')
        print(f'password2: {password2}')
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user)

    return render(
        request,
        'users/user_update.html',
        {'form': form, 'user': user}
    )


@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.user != user:
        messages.error(request, "У вас нет прав для изменения")
        return redirect('user_list')

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect('user_list')

    return render(request, 'users/user_delete.html', {'user': user})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы залогинены')
            return redirect('index')
        else:
            messages.error(request, 'Неверные данные пользователя или пароль.')
    return render(request, 'users/user_login.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'Вы разлогинены')
    return redirect('index')
