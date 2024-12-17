from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    UpdateView,
)


from task_manager.users.forms import (
    UserCreateForm,
    UserLoginForm,
    UserUpdateForm,
)
from task_manager.users.models import User


class UserBaseView:

    def handle_success_message(self, request, message):
        messages.success(request, message)

    def handle_error_message(self, request, message):
        messages.error(request, message)


class UserListView(UserBaseView, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(UserBaseView, CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.handle_success_message(self.request, 'Пользователь успешно зарегистрирован.')
        return super().form_valid(form)


class UserUpdateView(UserBaseView, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            self.handle_error_message(request, 'У вас нет прав для изменения')
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.handle_success_message(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserBaseView, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            self.handle_error_message(request, 'У вас нет прав для изменения')
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        self.handle_success_message(request, 'Пользователь успешно удален')
        return redirect('user_list')


class UserLoginView(UserBaseView, FormView):
    template_name = 'users/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('user_list')

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        login(self.request, form.get_user())
        self.handle_success_message(self.request, 'Вы залогинены')
        return redirect('index')

    def form_invalid(self, form):
        self.handle_error_message(self.request, 'Неверные данные пользователя или пароль.')
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(UserBaseView, View):
    def post(self, request):
        logout(request)
        self.handle_success_message(request, 'Вы разлогинены')
        return redirect('index')