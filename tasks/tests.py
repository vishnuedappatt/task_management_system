from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class TaskViewSetTestCase(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(
            email='admin@example.com', password='adminpassword')
        self.client.force_authenticate(user=self.admin_user)
        self.task = Task.objects.create(
            name="Sample Task", 
            type="PUBLIC", 
            owner=self.admin_user,
            due_date='2024-09-30'
        )
        self.task_url = reverse('task-detail', kwargs={'pk': self.task.id})

    def test_create_task(self):
        data = {
            "name": "New Task",
            "type": "PRIVATE",
            "due_date":'2024-09-30'
        }
        response = self.client.post(reverse('task-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task(self):
        data = {"name": "Updated Task", "type": "PRIVATE","due_date":'2024-09-30'}
        response = self.client.put(self.task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Task")

    def test_delete_task(self):
        response = self.client.delete(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_list_tasks(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



class GetAndUpdateTaskTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@example.com', password='userpassword')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            name="Sample Task", 
            type="PUBLIC", 
            owner=self.user,
            due_date='2024-09-30'
        )
        self.task_url = reverse('get or update individual task')

    def test_get_task(self):
        response = self.client.get(f'{self.task_url}?id={self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Sample Task")

    def test_update_task(self):
        data = {"name": "Updated Task"}
        response = self.client.put(f'{self.task_url}?id={self.task.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Task")

    def test_update_task_not_found(self):
        data = {"name": "Updated Task"}
        response = self.client.put(f'{self.task_url}?id=9999', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_task_not_found(self):
        response = self.client.get(f'{self.task_url}?id=9999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_permission_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'{self.task_url}?id={self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskListTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@example.com', password='userpassword',name="tester")
        self.client.force_authenticate(user=self.user)
        Task.objects.create(name="Task 1", type="PUBLIC", owner=self.user,due_date='2024-09-30')
        Task.objects.create(name="Task 2", type="PRIVATE", owner=self.user,due_date='2024-09-30')
        self.task_list_url = reverse('task list')

    def test_task_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_task_list_filter_by_type(self):
        response = self.client.get(self.task_list_url, {'type': 'PUBLIC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_task_list_filter_by_name(self):
        response = self.client.get(self.task_list_url, {'name': 'Task 2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)