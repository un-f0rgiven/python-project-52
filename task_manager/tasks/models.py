from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя задачи')
    description = models.TextField(blank=True, verbose_name='Описание задачи')
    status = models.ForeignKey(
        Status,
        related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name='Статус задачи'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks_created',
        verbose_name='Автор задачи'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )
    labels = models.ManyToManyField(
        Label, blank=True, related_name='tasks', verbose_name='Метки'
    )
    executor = models.ForeignKey(
        User,
        related_name='executors_tasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Исполнитель'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['pk']

    def __str__(self):
        return self.name
