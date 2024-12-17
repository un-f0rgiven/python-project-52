from task_manager.base_views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseUpdateView,
)
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelListView(BaseListView):
    model = Label
    template_name = 'labels/label_list.html'
    success_url = '/labels/'


class LabelCreateView(BaseCreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = '/labels/'

    def get_success_message(self):
        return 'Метка успешно создана.'
    
    def get_error_message(self):
        return 'Невозможно создать метку'


class LabelUpdateView(BaseUpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = '/labels/'

    def get_success_message(self):
        return 'Метка успешно изменена'
    
    def get_error_message(self):
        return 'Невозможно изменить метку'


class LabelDeleteView(BaseDeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = '/labels/'

    def get_success_message(self):
        return 'Метка успешно удалена'
    
    def get_error_message(self):
        return 'Невозможно удалить метку'