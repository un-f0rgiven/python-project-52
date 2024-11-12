from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from labels.models import Label
from tasks.models import Task
from statuses.models import Status

class LabelViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_label_list_view(self):
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')

    def test_label_create_view(self):
        response = self.client.post(reverse('label_create'), {'name': 'Test Label'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Test Label').exists())

    def test_label_update_view(self):
        label = Label.objects.create(name='Old Label')
        response = self.client.post(reverse('label_update', args=[label.pk]), {'name': 'Updated Label'})
        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, 'Updated Label')

    def test_label_delete_view(self):
        label = Label.objects.create(name='Label to Delete')
        response = self.client.post(reverse('label_delete', args=[label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name='Label to Delete').exists())

    def test_label_delete_view_with_tasks(self):
        status_new = Status.objects.create(name='new')

        label = Label.objects.create(name='Label with Task')
        task = Task.objects.create(title='Test Task', author=self.user, status=status_new)
        label.tasks.add(task)

        response = self.client.post(reverse('label_delete', args=[label.pk]))

        self.assertRedirects(response, reverse('label_list'))
        self.assertTrue(Label.objects.filter(name='Label with Task').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Невозможно удалить метку, т.к. она связана с задачей.', [msg.message for msg in messages])