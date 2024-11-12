import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task
from statuses.models import Status

@pytest.mark.django_db
class TestTaskCRUD:

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        client.login(username='testuser', password='password123')
        self.client = client

        # Создаем статус для использования в тестах
        self.status_new = Status.objects.create(name='new')
        self.status_in_progress = Status.objects.create(name='in_progress')

    def test_create_task(self):
        response = self.client.post(reverse('task_create'), {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'assignee': '',
            'status': self.status_new.id
        })

        assert response.status_code == 302
        assert Task.objects.count() == 1
        assert Task.objects.first().title == 'Test Task'

    def test_task_list(self):
        Task.objects.create(title='Test Task 1', author=self.user, status=self.status_new)
        Task.objects.create(title='Test Task 2', author=self.user, status=self.status_new)
        response = self.client.get(reverse('task_list'))
        assert response.status_code == 200
        assert 'Test Task 1' in response.content.decode()
        assert 'Test Task 2' in response.content.decode()

    def test_update_task(self):
        task = Task.objects.create(title='Old Title', author=self.user, status=self.status_new)
        response = self.client.post(reverse('task_update', args=[task.pk]), {
            'title': 'New Title',
            'description': 'Updated description.',
            'assigned_to': '',
            'status': self.status_in_progress.id
        })
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.title == 'New Title'

    def test_delete_task(self):
        task = Task.objects.create(title='Test Task to Delete', author=self.user, status=self.status_new)
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        assert response.status_code == 302
        assert Task.objects.count() == 0

    def test_task_detail(self):
        task = Task.objects.create(title='Detail Task', author=self.user, status=self.status_new)
        response = self.client.get(reverse('task_detail', args=[task.pk]))
        assert response.status_code == 200
        assert 'Detail Task' in response.content.decode()