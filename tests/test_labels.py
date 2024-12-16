from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

class LabelViewsTests(TestCase):
    fixtures = ['fixtures/initial_data.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='test_user')
        self.client.login(username='test_user', password='testpass')

        # Создаем метку для тестов
        self.label = Label.objects.create(name='Important')

    def test_label_list_view(self):
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertContains(response, self.label.name)

    def test_label_create_view(self):
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Метка успешно создана.', [m.message for m in messages_list]
        )

    def test_label_update_view(self):
        response = self.client.post(
            reverse('label_update', args=[self.label.pk]),
            {'name': 'Updated Label'}
        )
        self.label.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.label.name, 'Updated Label')
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Метка успешно изменена', [m.message for m in messages_list]
        )

    def test_label_delete_view(self):
        response = self.client.post(
            reverse('label_delete', args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Метка успешно удалена', [m.message for m in messages_list]
        )

    def test_label_delete_view_with_tasks(self):
        status = Status.objects.create(name='New Status')
        task = Task.objects.create(
            name='Test Task', author=self.user, status=status
        )
        task.labels.add(self.label)

        response = self.client.post(
            reverse('label_delete', args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Невозможно удалить метку, т.к. она связана с задачей.',
            [m.message for m in messages_list]
        )