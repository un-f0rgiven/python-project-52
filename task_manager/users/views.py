from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from task_manager.users.forms import UserCreateForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован.')
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(request, 'У вас недостаточно прав для изменения другого пользователя.')
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('user_list')
        return super(). dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Пользователь успешно удален')
        return response


class UserLoginView(FormView):
    template_name = 'users/user_login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'Вы залогинены')
        return redirect('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверные данные пользователя или пароль.')
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        return redirect('index')
