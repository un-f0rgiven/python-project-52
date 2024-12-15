from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class UserViewsTests(TestCase):
    fixtures = ['fixtures/initial_data.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='test_user')
        self.another_user = User.objects.get(username='another_test_user')

    def test_user_list_view(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertContains(response, 'test_first_name')

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'new_user',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertRedirects(response, reverse('user_login'))
        self.assertTrue(User.objects.filter(username='new_user').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован.')

    def test_user_update_view(self):
        self.client.login(username='test_user', password='testpass')
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'username': 'updated_user',
            'first_name': 'Updated',
            'last_name': 'User',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_user')
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_user_delete_other_user(self):
        self.client.login(username='test_user', password='testpass')
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.another_user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(pk=self.another_user.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Вы не можете удалить другого пользователя.')

    def test_user_delete_self(self):
        self.client.login(username='test_user', password='testpass')
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertRedirects(response, reverse('user_list'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Ваш аккаунт успешно удален.')

    def test_user_login_view(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'test_user',
            'password': 'testpass',
        })
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_logout_view(self):
        self.client.login(username='test_user', password='pbkdf2_sha256$870000$bgAfNBP3fmYuACcCr8ijb6$JFsSoBFJyCr+MredmYUpeVnNc/QKcxJ4rLP0/rziY/Q=')
        response = self.client.post(reverse('user_logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы разлогинены')