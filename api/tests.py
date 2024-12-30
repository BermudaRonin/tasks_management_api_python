from rest_framework.test import APITestCase
from rest_framework import status
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Task, User

class APITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

        self.task = Task.objects.create(
            title='Sample Task',
            description='Task Description',
            owner=self.user,
            status=Task.Status.PENDING,
        )

    # --- Authentication Tests ---

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'Bw0dJ@example.com',
            'password': 'newpass123',
        }
        response = self.client.post('/api/auth/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        data = {
            'username': 'testuser',
            'password': 'password123',
        }
        response = self.client.post('/api/auth/login', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post('/api/auth/login', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- User Management Tests ---

    def test_get_current_user(self):
        response = self.client.get('/api/user')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_current_user(self):
        data = {'username': 'updateduser'}
        response = self.client.put('/api/user', data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_current_user(self):
        response = self.client.delete('/api/user')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Tasks Management Tests ---

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'Task description',
        }
        response = self.client.post('/api/tasks', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # --- Task Management Tests ---

    def test_get_task_by_id(self):
        response = self.client.get(f'/api/task/{self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Task')

    def test_update_task(self):
        data = {'title': 'Updated Task'}
        response = self.client.put(f'/api/task/{self.task.id}', data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_complete_task(self):
        response = self.client.put(f'/api/task/{self.task.id}/complete')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_uncomplete_task(self):
        self.task.status = Task.Status.COMPLETED
        self.task.save()
        response = self.client.put(f'/api/task/{self.task.id}/pending')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task(self):
        response = self.client.delete(f'/api/task/{self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
