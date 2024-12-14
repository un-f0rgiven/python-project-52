from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskViewsTests(TestCase):
    fixtures = ['fixtures/initial_data.json']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.client.login(username='testuser', password='testpass')

        self.status = Status.objects.create(name='New')
        self.label = Label.objects.create(name='Important')

        self.task = Task.objects.create(
            title='Test Task',
            author=self.user,
            status=self.status,
        )
        self.task.labels.add(self.label)

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, self.task.title)

    def test_task_create_view(self):
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'status': self.status.id,
            'labels': [self.label.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Задача успешно создана',
            [m.message for m in messages_list]
        )

    def test_task_update_view(self):
        response = self.client.post(
            reverse('task_update', args=[self.task.pk]),
            {
                'title': 'Updated Task',
                'status': self.status.id,
                'labels': [self.label.id],
            }
        )
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.title, 'Updated Task')
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Задача успешно изменена.',
            [m.message for m in messages_list]
        )

    def test_task_delete_view(self):
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Задача успешно удалена.',
            [m.message for m in messages_list]
        )

    def test_task_delete_view_no_permission(self):
        User.objects.create_user(username='otheruser', password='otherpass')
        self.client.logout()
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Задачу может удалить только ее автор',
            [m.message for m in messages_list]
        )