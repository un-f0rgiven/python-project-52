from django.db import models
from django.contrib.auth.models import User
from labels.models import Label
from statuses.models import Status

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, related_name='tasks', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    labels = models.ManyToManyField(Label, blank=True, related_name='tasks')
    executor = models.ForeignKey(User, related_name='executors_tasks', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title