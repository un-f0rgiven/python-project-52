from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status

class StatusViewTest(TestCase):
    fixtures = ['statuses.json']

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_status_list_view(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'новый')
        self.assertContains(response, 'в работе')
        self.assertContains(response, 'на тестировании')
        self.assertContains(response, 'завершен')

    def test_status_create_view(self):
        response = self.client.post(reverse('status_create'), {'name': 'в процессе'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='в процессе').exists())

    def test_status_update_view(self):
        status = Status.objects.get(pk=1)
        response = self.client.post(reverse('status_update', args=[status.pk]), {'name': 'обновленный'})
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, 'обновленный')

    def test_status_delete_view(self):
        status = Status.objects.get(pk=1)
        response = self.client.post(reverse('status_delete', args=[status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())