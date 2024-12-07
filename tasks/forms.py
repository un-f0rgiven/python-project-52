from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'labels', 'executor']
        widgets = {
            'labels': forms.CheckboxSelectMultiple(
                attrs={'id': 'id_labels'})
        }
