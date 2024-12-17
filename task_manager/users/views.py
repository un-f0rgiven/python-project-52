from django.contrib import messages
from django.contrib.auth import login, logout
from task_manager.users.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.users.forms import UserCreateForm, UserUpdateForm, UserLoginForm


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
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
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        print('Вызывается Method dispatch')
        user = self.get_object()
        
        if request.user != user:
            messages.error(request, 'Вы не можете удалить другого пользователя.')
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('Вызывается Method POST')
        user = self.get_object()
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect('user_list')


class UserLoginView(FormView):
    template_name = 'users/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('user_list')

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
