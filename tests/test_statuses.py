from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusViewsTests(TestCase):
    fixtures = ['fixtures/initial_data.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='test_user')
        self.client.login(username='test_user', password='testpass')

        # Создаем статус для тестов
        self.status = Status.objects.create(name='New Status')

    def test_status_list_view(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_list.html')
        self.assertContains(response, self.status.name)

    def test_status_create_view(self):
        response = self.client.post(reverse('status_create'), {
            'name': 'In Progress'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='In Progress').exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Статус успешно создан',
            [m.message for m in messages_list]
        )

    def test_status_update_view(self):
        response = self.client.post(
            reverse('status_update', args=[self.status.pk]),
            {
                'name': 'Updated Status'
            }
        )
        self.status.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.status.name, 'Updated Status')
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Статус успешно изменен',
            [m.message for m in messages_list]
        )

    def test_status_delete_view(self):
        response = self.client.post(
            reverse('status_delete', args=[self.status.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Статус успешно удален',
            [m.message for m in messages_list]
        )