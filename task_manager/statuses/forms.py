from django import forms

from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, label='Имя')

    class Meta:
        model = Status
        fields = ['name']
