from task_manager.base_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status

class StatusListView(BaseListView):
    model = Status
    template_name = 'statuses/status_list.html'
    success_url = '/statuses/'

class StatusCreateView(BaseCreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_create.html'
    success_url = '/statuses/'

    def get_success_message(self):
        return 'Статус успешно создан'
    
    def get_error_message(self):
        return 'Невозможно создать статус'

class StatusUpdateView(BaseUpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = '/statuses/'

    def get_success_message(self):
        return 'Статус успешно изменен'
    
    def get_error_message(self):
        return 'Невозможно изменить статус'

class StatusDeleteView(BaseDeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = '/statuses/'

    def get_success_message(self):
        return 'Статус успешно удален'
    
    def get_error_message(self):
        return 'Невозможно удалить статус'