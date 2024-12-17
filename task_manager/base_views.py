from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class BaseListView(ListView):
    context_object_name = 'items'


class BaseCreateView(CreateView):
    
    def form_valid(self, form):
        messages.success(self.request, self.get_success_message())
        return super().form_valid(form)

    def get_success_message(self):
        return f'{self.model.__name__} успешно создан.'


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    
    def form_valid(self, form):
        messages.success(self.request, self.get_success_message())
        return super().form_valid(form)

    def get_success_message(self):
        return f'{self.model.__name__} успешно изменен.'


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if hasattr(self.object, 'tasks') and self.object.tasks.exists():
            messages.error(request, self.get_error_message())
            return redirect(self.get_success_url())

        messages.success(request, self.get_success_message())
        return super().delete(request, *args, **kwargs)

    def get_success_message(self):
        return f'{self.model.__name__} успешно удален.'

    def get_error_message(self):
        return f'Невозможно удалить {self.model.__name__.lower()}.'