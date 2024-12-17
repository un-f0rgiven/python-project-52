import django_filters

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label='Статус', queryset=Status.objects.all()
    )
    executor = django_filters.ModelChoiceFilter(
        label='Исполнитель', queryset=User.objects.all()
    )
    labels = django_filters.ModelChoiceFilter(
        label='Метка', queryset=Label.objects.all()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskFilter, self).__init__(*args, **kwargs)

    def filter_queryset(self, queryset):
        if self.data.get('self_tasks') == 'on':
            queryset = queryset.filter(author=self.user)
        return super().filter_queryset(queryset)
    
    def label_from_instance(self, obj):
        return str(obj)