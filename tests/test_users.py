from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


class UserViewsTests(TestCase):
    fixtures = ['fixtures/initial_data.json']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.another_user = User.objects.get(username='anothertestuser')

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertContains(response, self.user.username)

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Пользователь успешно зарегистрирован.',
            [m.message for m in messages_list]
        )

    def test_user_update_view_as_owner(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('user_update', args=[self.user.pk]),
            {
                'username': 'updateduser',
                'password': 'testpass',
                'password2': 'testpass'
            }
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, 'updateduser')
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Пользователь успешно изменен',
            [m.message for m in messages_list]
        )

    def test_user_update_view_as_other_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('user_update', args=[self.another_user.pk]),
            {
                'username': 'malicious_update',
                'password': 'testpass',
                'password2': 'testpass'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(self.another_user.username, 'malicious_update')
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'У вас недостаточно прав для изменения другого пользователя.',
            [m.message for m in messages_list]
        )

    def test_user_delete_view_as_owner(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Пользователь успешно удален',
            [m.message for m in messages_list]
        )

    def test_user_delete_view_as_other_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete', args=[self.another_user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='anothertestuser').exists())
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            'У вас нет прав для изменения',
            [m.message for m in messages_list]
        )

    def test_user_login_view(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Вы залогинены', [m.message for m in messages_list])

    def test_user_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Вы разлогинены', [m.message for m in messages_list])