from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelBaseView(LoginRequiredMixin):
    model = Label
    form_class = LabelForm
    success_url = 'label_list'

    def get_success_url(self):
        return reverse(self.success_url)


class LabelCreateView(LabelBaseView, CreateView):
    template_name = 'labels/label_create.html'

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно создана.')
        return super().form_valid(form)


class LabelUpdateView(LabelBaseView, UpdateView):
    template_name = 'labels/label_update.html'

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно изменена')
        return super().form_valid(form)


class LabelDeleteView(LabelBaseView, DeleteView):
    template_name = 'labels/label_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.object.tasks.exists():
            messages.error(request, 'Невозможно удалить метку')
            return redirect(self.get_success_url())

        messages.success(request, 'Метка успешно удалена')
        return super().delete(request, *args, **kwargs)
