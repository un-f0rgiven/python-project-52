from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from labels.models import Label
from django.contrib.messages import get_messages


class LabelViewsTests(TestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

        # Создание тестовой метки
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
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
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
        # Создание статуса, который будет использоваться в задаче
        from statuses.models import Status  # Импортируем модель статуса
        status = Status.objects.create(name='New Status')

        # Создание задачи и связывание с меткой
        from tasks.models import Task  # Импортируем модель задачи
        task = Task.objects.create(
            title='Test Task', author=self.user, status=status
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
