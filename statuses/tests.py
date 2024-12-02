from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status
from statuses.forms import StatusForm
from django.contrib import messages
from django.contrib.messages import get_messages

class StatusViewsTests(TestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Создание тестового статуса
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
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        self.assertTrue(Status.objects.filter(name='In Progress').exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Статус успешно создан', [m.message for m in messages_list])

    def test_status_update_view(self):
        response = self.client.post(reverse('status_update', args=[self.status.pk]), {
            'name': 'Updated Status'
        })
        self.status.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.status.name, 'Updated Status')
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Статус успешно изменен', [m.message for m in messages_list])

    def test_status_delete_view(self):
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Статус успешно удален', [m.message for m in messages_list])