from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager.base_views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseUpdateView,
)
from task_manager.users.forms import (
    UserCreateForm,
    UserLoginForm,
    UserUpdateForm,
)
from task_manager.users.models import User


class UserListView(BaseListView):
    model = User
    template_name = 'users/user_list.html'
    success_url = reverse_lazy('user_list') 


class UserCreateView(BaseCreateView):
    form_class = UserCreateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')

    def get_success_message(self):
        return 'Пользователь успешно зарегистрирован.'
    
    def get_error_message(self):
        return 'Невозможно изменить пользователя'


class UserUpdateView(BaseUpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj:
            messages.error(
                request, "У вас нет прав для изменения другого пользователя."
            )
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)

    def get_success_message(self):
        return 'Пользователь успешно изменен'


class UserDeleteView(BaseDeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj:
            messages.error(
                request, "У вас нет прав для изменения другого пользователя."
            )
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)

    def get_success_message(self):
        return 'Пользователь успешно удален'


class UserLoginView(LoginView):
    template_name = 'users/user_login.html'
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('user_login') 

    def get_success_url(self):
        messages.success(self.request, 'Вы разлогинены')
        return reverse_lazy('index')
    