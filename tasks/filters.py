import django_filters
from .models import Task, Status, User, Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    executor = django_filters.ChoiceFilter()
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all())

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super(TaskFilter, self).__init__(*args, **kwargs)
        self.form.fields['status'].label = 'Статус'
        self.form.fields['executor'].label = 'Исполнитель'
        self.form.fields['labels'].label = 'Метка'

        self.form.fields['status'].widget.attrs.update(
            {'class': 'form-select', 'placeholder': 'Статус'}
        )
        self.form.fields['executor'].widget.attrs.update(
            {'class': 'form-select', 'placeholder': 'Исполнитель'}
        )
        self.form.fields['labels'].widget.attrs.update(
            {'class': 'form-select', 'placeholder': 'Метка'}
        )

        if 'status' in self.data:
            self.form.fields['status'].widget.attrs['class'] += ' is-valid'
        if 'executor' in self.data:
            self.form.fields['executor'].widget.attrs['class'] += ' is-valid'
        if 'labels' in self.data:
            self.form.fields['labels'].widget.attrs['class'] += ' is-valid'

        executors = User.objects.all()
        self.form.fields['executor'].choices = [
            (
                executor.pk,
                f"{executor.first_name} {executor.last_name}"
            ) for executor in executors
        ]

        if 'executor' in self.data:
            self.form.fields['executor'].widget.attrs['class'] += ' is-valid'

    def filter_queryset(self, queryset):
        executor_id = self.data.get('executor')
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        return super().filter_queryset(queryset)
