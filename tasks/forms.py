from django import forms
from tasks.models import Task
from labels.models import Label

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'labels']
        widgets = {'labels': forms.CheckboxSelectMultiple(),}