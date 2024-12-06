import django_filters
from .models import Task, Status, User, Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all())

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
    

    def __init__(self, *args, **kwargs):
        super(TaskFilter, self).__init__(*args, **kwargs)
        self.form.fields['status'].label = 'Статус'
        self.form.fields['executor'].label = 'Исполнитель'
        self.form.fields['labels'].label = 'Метка'

        self.form.fields['status'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Статус'})
        self.form.fields['executor'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Исполнитель'})
        self.form.fields['labels'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Метка'})

        if 'status' in self.data:
            self.form.fields['status'].widget.attrs['class'] += ' is-valid'
        if 'executor' in self.data:
            self.form.fields['executor'].widget.attrs['class'] += ' is-valid'
        if 'labels' in self.data:
            self.form.fields['labels'].widget.attrs['class'] += ' is-valid'