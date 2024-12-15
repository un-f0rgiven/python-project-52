from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = '/labels/'
    
    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно создана.')
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = '/labels/'

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно изменена')
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = '/labels/'

    def dispatch(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(
                request,
                'Невозможно удалить метку, т.к. она связана с задачей.'
            )
            return redirect('label_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Метка успешно удалена')
        return super().delete(request, *args, **kwargs)