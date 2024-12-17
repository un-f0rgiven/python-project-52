from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusBaseView(LoginRequiredMixin):
    model = Status
    form_class = StatusForm
    success_url = 'status_list'

    def get_success_url(self):
        return reverse(self.success_url)


class StatusCreateView(StatusBaseView, CreateView):
    template_name = 'statuses/status_create.html'

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(StatusBaseView, UpdateView):
    template_name = 'statuses/status_update.html'

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен')
        return super().form_valid(form)


class StatusDeleteView(StatusBaseView, DeleteView):
    template_name = 'statuses/status_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.object.tasks.exists():
            messages.error(request, 'Невозможно удалить статус')
            return redirect(self.get_success_url())

        messages.success(request, 'Статус успешно удален')
        return super().delete(request, *args, **kwargs)
