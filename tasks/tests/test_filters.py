from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from statuses.models import Status
from labels.models import Label

class TaskListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.status1 = Status.objects.create(name='Pending')
        self.status2 = Status.objects.create(name='Completed')

        self.label1 = Label.objects.create(name='Important')
        self.label2 = Label.objects.create(name='Urgent')

        self.task1 = Task.objects.create(title='Task 1', author=self.user, status=self.status1)
        self.task2 = Task.objects.create(title='Task 2', author=self.user, status=self.status2, assignee=self.user)
        self.task3 = Task.objects.create(title='Task 3', author=self.user, status=self.status1)
        self.task4 = Task.objects.create(title='Task 4', author=self.user, status=self.status2, assignee=self.user)
        
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.task5 = Task.objects.create(title='Task 5', author=self.other_user, status=self.status1)

    def test_task_list_view_only_shows_user_tasks(self):
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
        self.assertContains(response, 'Task 3')
        self.assertContains(response, 'Task 4')
        self.assertNotContains(response, 'Task 5')

    def test_filter_by_status(self):
        response = self.client.get(reverse('task_list'), {'status': self.status1.id})
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 4')

    def test_filter_by_assignee(self):
        response = self.client.get(reverse('task_list'), {'assignee': self.user.id})
        self.assertContains(response, 'Task 2')
        self.assertContains(response, 'Task 4')
        self.assertNotContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 3')

    def test_filter_by_label(self):
        self.task1.labels.add(self.label1)
        self.task2.labels.add(self.label2)

        response = self.client.get(reverse('task_list'), {'label': self.label1.id})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')