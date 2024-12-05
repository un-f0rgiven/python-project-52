from django import forms
from tasks.models import Task
from labels.models import Label

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'labels', 'executor']
        widgets = {'labels': forms.CheckboxSelectMultiple(),}