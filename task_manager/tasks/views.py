from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.all()
        task_filter = TaskFilter(self.request.GET, queryset=tasks)

        if self.request.GET.get('self_tasks'):
            tasks = tasks.filter(author=self.request.user)

        return task_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TaskFilter(self.request.GET, queryset=self.get_queryset())
        context['statuses'] = Status.objects.all()
        context['labels'] = Label.objects.all()
        context['executors'] = User.objects.all()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = '/tasks/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = '/tasks/'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('task_list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Задача успешно удалена.')
        return super().delete(request, *args, **kwargs)


class TaskShowView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_show.html'