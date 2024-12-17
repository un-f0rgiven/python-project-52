from django.views.generic.detail import DetailView
from task_manager.base_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class TaskListView(BaseListView):
    model = Task
    template_name = 'tasks/task_list.html'
    success_url = '/tasks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TaskFilter(self.request.GET, user=self.request.user)
        context['object_list'] = context['filter'].qs
        return context

class TaskCreateView(BaseCreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = '/tasks/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self):
        return 'Задача успешно создана'
    
    def get_error_message(self):
        return 'Невозможно создать задачу'

class TaskUpdateView(BaseUpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = '/tasks/'

    def get_success_message(self):
        return 'Задача успешно изменена.'
    
    def get_error_message(self):
        return 'Невозможно изменить задачу'

class TaskDeleteView(UserPassesTestMixin, BaseDeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = '/tasks/'

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if not self.test_func():
            messages.error(request, "Задачу может удалить только ее автор")
            return redirect(reverse('task_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_message(self):
        return 'Задача успешно удалена.'
    
    def get_error_message(self):
        return 'Невозможно удалить задачу'

class TaskShowView(DetailView):
    model = Task
    template_name = 'tasks/task_show.html'
    context_object_name = 'task'
