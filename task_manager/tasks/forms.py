from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, label='Имя')
    description = forms.CharField(max_length=250, required=True, label='Описание', widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize: vertical;'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус', empty_label="---------")
    executor = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='Исполнитель', empty_label="---------")
    labels = forms.ModelMultipleChoiceField(queryset=Label.objects.all(), required=False, label='Метки', widget=forms.SelectMultiple())

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

